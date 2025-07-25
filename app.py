import streamlit as st
import openai
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate  # Correct import
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# LangSmith Tracking
os.environ['LANGCHAIN_API_KEY'] = os.getenv('LANGCHAIN_API_KEY')
os.environ['LANGCHAIN_PROJECT_V2'] = "true"
os.environ["LANGCHAIN_PROJECT"] = "Chatbot"

# Prompt template (fixed usage of from_messages, not from_message)
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant. Please respond to the user's questions."),
        ("user", "Question: {question}"),
    ]
)

# Function to generate response
def generate_response(question, api_key, llm_model, temperature, max_tokens):
    openai.api_key = api_key
    llm = ChatOpenAI(model=llm_model, temperature=temperature, max_tokens=max_tokens)
    output_parser = StrOutputParser()
    chain = prompt | llm | output_parser
    answer = chain.invoke({"question": question})
    return answer

# Title of the app
st.title("🧠 Enhanced Q&A Chatbot with OpenAI")

# Sidebar for settings
st.sidebar.title("Settings")
api_key = st.sidebar.text_input("Enter your OpenAI API key", type="password")
llm_model = st.sidebar.selectbox("Select an OpenAI model", ["gpt-4o", "gpt-4-turbo", "gpt-4"])
temperature = st.sidebar.slider("Temperature", 0.0, 1.0, 0.5)
max_tokens = st.sidebar.slider("Max tokens", 50, 300, 150)

# Main interface for user input
st.write("Enter your question below:")

user_input = st.text_input("You:")

if user_input:
    if not api_key:
        st.warning("Please enter your OpenAI API key to continue.")
    else:
        response = generate_response(user_input, api_key, llm_model, temperature, max_tokens)
        st.write("Assistant:", response)
