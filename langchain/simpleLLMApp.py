import os
from dotenv import load_dotenv
load_dotenv()
from langchain_community.llms import Ollama
import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


## Loading OpenAI Key
os.environ['OPENAI_API_KEY'] = os.getenv("OPENAI_API_KEY")
## Loading Langchain Key
os.environ['LANGCHAIN_API_KEY'] = os.getenv("LANGCHAIN_API_KEY")
os.environ['LANGCHAIN_TRACING_V2'] = "true"
os.environ['LANGCHAIN_PROJECT'] = os.getenv("LANGCHAIN_PROJECT")


## Prompt Tempelate

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are an helpful assistant. Respond to my questions."),
        ("user","Question:{question}")
    ]
)


## Setting Up streamlit

st.title("Langchain App with Ollama")
input_text = st.text_input("What's your question?")


llm = Ollama(model = "mistral")
output_parser = StrOutputParser()
chain = prompt|llm|output_parser


if input_text:
    response = chain.invoke({"question":input_text})

st.write(response)