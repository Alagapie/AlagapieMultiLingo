
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
import streamlit as st

st.set_page_config(
    page_icon=":brain:",
    page_title="Alagapie Translator app",
    layout="centered"
)
api_key = st.secrets["general"]["GOOGLE_API_KEY"]
model=ChatGoogleGenerativeAI(model="gemini-1.5-flash",temperature=0.9,google_api_key=api_key)

def generate_promp(chat_history, input_language, output_language, input_text):
    messages = [
        ("system", f"You are a helpful assistant that translates {input_language} to {output_language}.")
    ]
    messages.extend(chat_history)
    messages.append(("human", input_text))
    
    return ChatPromptTemplate.from_messages(messages)

# Function to perform translation
def translate(input_language, output_language, input_text):
    prompt = generate_promp(st.session_state.translation_chat_history, input_language, output_language, input_text)
    chain = prompt | model
    response = chain.invoke(
        {
            "input_language": input_language,
            "output_language": output_language,
            "input": input_text
        }
    )
    return response.content


st.title("🌐 Alagapie MultiLingo")

# Initialize chat session in Streamlit if not already present
if 'translation_chat_history' not in st.session_state:
     st.session_state.translation_chat_history= []

# Input for languages and text
col1, col2 = st.columns(2)
with col1:
      input_languages_list = ["English", "French", "German", "Latin", "Spanish", "Arabic", "Chinese", "Japanese", "Korean", "Russian", "Portuguese", "Italian", "Dutch"]

      input_language = st.selectbox(label="CHOOSE THE LANGUAGE YOU WANT TO TRANSLATE ", options=input_languages_list)

with col2:
       output_languages_list = [x for x in input_languages_list if x != input_language]
       output_language = st.selectbox(label="CHOOSE THE LANGUAGE TO TRANSLATE TO  ", options=output_languages_list)

input_text = st.chat_input("input text to translate")
if st.button("Start a New Chat"):
      st.session_state.translation_chat_history= []

# Handle translation and chat history
if input_text:
    # Add user's message to chat history
       st.session_state.translation_chat_history.append(("human", input_text))
    
    # Perform translation
       with st.spinner("Translating..."):
                # Perform translation
                translation = translate(input_language, output_language, input_text)
    
    # Add translation result to chat history
       st.session_state.translation_chat_history.append(("assistant", translation))
    
    # Display the result
   

# Display chat history
for role, message in st.session_state.translation_chat_history:
       with st.chat_message(role):
        st.markdown(message)
 
