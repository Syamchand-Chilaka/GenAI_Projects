import os
import streamlit as st 
from langchain.agents import create_sql_agent
from langchain.sql_database import SQLDatabase
from langchain.agents.agent_types import AgentType
from langchain.callbacks import StreamlitCallbackHandler
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from sqlalchemy import create_engine
import sqlite3
from pathlib import Path
from langchain_groq import ChatGroq


st.set_page_config(page_title="Langchain: Chat with SQL")
st.title("Langchain: Chat with SQL DB")

INJECTION_WARNING = """
    SQL agent can be vulnerable to prompt injection.
    """
    
LOCALDB = "USE_LOCALDB"
MYSQL = "USE_MYSQL"

llm = None

radio_opt = ["Use SQLLite3 Database - Student.db", "Connect to your SQL Database"]

selected_opt = st.sidebar.radio(label="Choose the Database", options=radio_opt)

if radio_opt.index(selected_opt)==1:
    db_uri = MYSQL
    mysql_host = st.sidebar.text_input("Provide MySQL Host:")
    mysql_user = st.sidebar.text_input("MySQL Username:")
    mysql_password = st.sidebar.text_input("MySQL Password:", type="password")
    mysql_db = st.sidebar.text_input("MySQL Database:")
    
else:
    db_uri=LOCALDB
    
    
groq_api_key = st.sidebar.text_input("Groq API Key:", type="password")

if not db_uri:
    st.info("Please select a Database")

if not groq_api_key:
    st.info("Please enter the Groq API Key")
    
if groq_api_key:
    llm = ChatGroq(groq_api_key= groq_api_key, model_name="Llama3-8b-8192", streaming=True)

@st.cache_resource(ttl="2h")
def configure_db(db_uri, mysql_user=None,mysql_host=None, mysql_password=None, mysql_db=None):
    if db_uri==LOCALDB:
        db_filepath=(Path(__file__).parent/"student.db").absolute()
        print(db_filepath)
        creator = lambda: sqlite3.connect(f"file:{db_filepath}?mode=ro", uri=True)
        return SQLDatabase(create_engine("sqlite:///", creator=creator))
    elif db_uri==MYSQL:
        if not (mysql_host and mysql_db and mysql_user and mysql_password):
            st.error("Please provide all MySQL connection details.")
            st.stop()
            
        return SQLDatabase(create_engine(f"mysql+mysqlconnector://{mysql_user}:{mysql_password}@{mysql_host}/{mysql_db}"))
    
    
if db_uri==MYSQL:
    db=configure_db(db_uri,mysql_user, mysql_host, mysql_password, mysql_db)
elif db_uri==LOCALDB:
    db=configure_db(db_uri)



##### Toolkit
if llm:
    tool_kit=SQLDatabaseToolkit(db=db, llm=llm)

    agent = create_sql_agent(
        llm= llm,
        toolkit= tool_kit,
        verbose= True,
        agent_type= AgentType.ZERO_SHOT_REACT_DESCRIPTION
    )

    if "messages" not in st.session_state or st.sidebar.button("Clear message history"):
        st.session_state["messages"] = [
            {"role":"assisstant", "content":"Hi, I am a chatbot who can search the web. How can I help you?"}
        ]
        
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])
        
    user_query = st.chat_input(placeholder="Ask questions from Database")

    if user_query:
        st.session_state.messages.append({"role":"user", "content": user_query})
        st.chat_message("user").write(user_query)
        
        with st.chat_message("assisstant"):
            streamlit_callback = StreamlitCallbackHandler(st.container())
            response = agent.run(user_query, callbacks=[streamlit_callback])
            st.session_state.messages.append({"role":"assisstant", "content":response})
            st.write(response)