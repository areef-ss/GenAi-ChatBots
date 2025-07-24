import streamlit as st
import openai
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core import ChatPromptTemplate


import os
from dotenv import load_dotenv
load_dotenv()

##LsngSmith tracking

os.environ['LANGCHAIN_API_KEY'] = os.getenv('LANGCHAIN_API_KEY')
os.environ['LANGCHAIN_PROJECT_V2'] ="true"
os.environ["LANGCHAIN_PROJECT"] = "Chatbot"


#prompt template

pompt=ChatPromptTemplate.from_message(
    [
        ("system","you are a helpful assistant.pleae responce to the user's questions"),
        ("user","Question:{question}"),
    ]
)


def generate_response(question,api_key,llm,temperates,max_tokens):
    openai.api_key=api_key
    llm=ChatOpenAI(model=llm)
    output_parseer=StrOutputParser()
    chain=pompt | llm |output_parseer
    answer=chain.invoke({"question":question})
    return answer


##Title of the app

st.title("Enchanced Q&A Chatbot with OpenAI")

##Sidebar for settigs

st.sidebar.title("Settings")
api_key=st.sidebar.text_input("Enter your OpenAI API key",type="password")
llm=st.sidebar.selection("Select adn open Ai model",["gpt-4o","gpt-4-turbo","gpt-4"])

temperature=st.sidebar.slider("Enter the temperature",0.0,1.0,0.5)
max_tokens=st.sidebar.slider("Enter the max tokens",50,300,150)

##Main interface for uiser input

st.write("Enter your question")

user_input=st.text_input("you:")

if user_input:
    responce=generate_response(user_input,api_key,llm,temperature,max_tokens)
    st.write(responce)





