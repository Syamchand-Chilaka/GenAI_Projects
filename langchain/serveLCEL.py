from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
import os
from langserve import add_routes
from dotenv import load_dotenv
load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")

model = ChatGroq(model="gemma2-9b-it",groq_api_key= groq_api_key)

generic_template = "Convert the following into {language}"

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", generic_template), ("user","{text}")
    ]
)

parser  = StrOutputParser()

chain = prompt|model|parser

##APP Defination

app = FastAPI(title="Langchain",
              version="1.0",
              description="Langchain Interface")

add_routes(
    app,
    chain,
    path="/chain"
)

if __name__=="__main__":
    import uvicorn
    uvicorn.run(app, host="localhost",port=8000)