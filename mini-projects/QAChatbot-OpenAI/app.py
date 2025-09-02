import os
import openai
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from dotenv import load_dotenv
load_dotenv(dotenv_path="../.env")


### LangSmith Tracking
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = os.getenv("LANGCHAIN_PROJECT")



### Creating the Prompt Template
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assisstant. Please respond to queries."),
        ("user", "Question:{question}")
    ]
)


def generate_response(question, api_key, engine, temperature, max_tokens):
    openai.api_key = api_key
    llm = ChatOpenAI(model = engine)
    output_parser = StrOutputParser()
    chain = prompt|llm|output_parser
    answer = chain.invoke({"question":question})
    return answer


### Creating the App

st.title("Q&A ChatBot with OpenAI")


##### Creating the SideBar

st.sidebar.title("Settings")
api_key = st.sidebar.text_input("Enter your OpenAI API Key:", type="password")


### Drop Down to select model
engine = st.sidebar.selectbox("Select an Open AI Model", ["gpt-4o","gpt-4-turbo","gpt-4o-mini"])

#### Parameters
temperature = st.sidebar.slider("Temperature", min_value=0.0, max_value=1.0, value=0.6)
max_tokens = st.sidebar.slider("Max Tokens", min_value=50, max_value=300, value=150)

## Main Interface
st.write("Go ahead and Ask Your Question")
user_input = st.text_input("Question:")

if user_input:
    if api_key:
        response = generate_response(user_input, api_key, engine, temperature, max_tokens)
        st.write(response)
    else:
        st.write("Please give API Key")

