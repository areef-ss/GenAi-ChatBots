from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.llms import Ollama
import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

##Langsmith tracing
LANGSMITH_TRACING="true"

LANGSMITH_ENDPOINT="https://api.smith.langchain.com"
LANGSMITH_API_KEY="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"
LANGSMITH_PROJECT="Simpel @ & A with ollama"
OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")
import openai
from langsmith.wrappers import wrap_openai
from langsmith import traceable

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant. Please respond to the user's questions."),
        ("user", "Question: {question}"),
    ]
)

# Function to generate response
def generate_response(question, llm_model, temperature, max_tokens):
    llm = Ollama(model=llm_model, temperature=temperature)
    output_parser = StrOutputParser()
    chain = prompt | llm | output_parser
    answer = chain.invoke({"question": question})
    return answer

st.title("🧠 Enhanced Q&A Chatbot with OpenAI")

# Sidebar for settings
st.sidebar.title("Settings")
llm_model = st.sidebar.selectbox("Select an OpenAI model", ["llama3"])
temperature = st.sidebar.slider("Temperature", 0.0, 1.0, 0.5)
max_tokens = st.sidebar.slider("Max tokens", 50, 300, 150)

# Main interface for user input
st.write("Enter your question below:")

user_input = st.text_input("You:")

if user_input:
    response = generate_response(user_input,llm_model, temperature, max_tokens)
    st.write("Assistant:", response)