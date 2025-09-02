import os
import time
import streamlit as st
from langchain_groq import ChatGroq
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFDirectoryLoader
from dotenv import load_dotenv
load_dotenv(dotenv_path="../.env")

groq_api_key = os.getenv("GROQ_API_KEY")

llm = ChatGroq(groq_api_key= groq_api_key, model_name = "Llama3-8b-8192")


prompt = ChatPromptTemplate.from_template(
    """
    Answer the questions based on the provided Context only.
    Please provide the most accurate response based on the question.
    
    Context:{context}
    
    Question:{input}
    """
)


def create_vector_embeddings():
    if "vectors" not in st.session_state:
        st.session_state.embeddings = OpenAIEmbeddings()
        st.session_state.loader = PyPDFDirectoryLoader("../data")
        st.session_state.docs= st.session_state.loader.load()
        st.session_state.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap =200)
        st.session_state.final_documents = st.session_state.text_splitter.split_documents(st.session_state.docs)
        st.session_state.vectors = FAISS.from_documents(st.session_state.final_documents, st.session_state.embeddings)
        
        
        
user_prompt = st.text_input("Enter your query for research paper:")

if st.button("Document Embedding"):
    create_vector_embeddings()
    st.write("Vector Database is Ready")
    
    
if user_prompt:
    documents_chain = create_stuff_documents_chain(llm,prompt)
    retriever = st.session_state.vectors.as_retriever()
    chain = create_retrieval_chain(retriever, documents_chain)
    response = chain.invoke({"input":user_prompt})
    
    st.write(response["answer"])
    with st.expander("Document Similarity Search"):
        for i, doc in enumerate(response["context"]):
            st.write(doc.page_content)
            st.write("-------------------------------------------------------")