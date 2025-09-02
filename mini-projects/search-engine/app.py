import streamlit as st
from langchain_community.utilities import ArxivAPIWrapper, WikipediaAPIWrapper
from langchain_community.tools import ArxivQueryRun, WikipediaQueryRun, DuckDuckGoSearchRun
from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent, AgentType
from langchain.callbacks import StreamlitCallbackHandler
import os
from dotenv import load_dotenv



api_wrapper_wiki = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=500)
wiki_tool = WikipediaQueryRun(api_wrapper=api_wrapper_wiki)

api_wrapper_arxiv = ArxivAPIWrapper(top_k_results=1, doc_content_chars_max=500)
arxiv_tool = ArxivQueryRun(api_wrapper = api_wrapper_arxiv)

search = DuckDuckGoSearchRun(name="search")


### Creating the App

st.title("Search Engine")


##### Creating the SideBar

st.sidebar.title("Settings")
api_key = st.sidebar.text_input("Enter your OpenAI API Key:", type="password")
os.environ["OPENAI_API_KEY"] = api_key

### Drop Down to select model
engine = st.sidebar.selectbox("Select an Open AI Model", ["gpt-4o","gpt-4-turbo","gpt-4o-mini"])



if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role":"assisstant", "content":"Hi, I am a chatbot who can search the web. How can I help you?"}
    ]
    
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])
    
    
if prompt:=st.chat_input(placeholder="What is Machine Learning?"):
    st.session_state.messages.append({"role": "user", "content":"prompt"})
    st.chat_message("user").write(prompt)
    llm = ChatOpenAI(model= engine, streaming=True)
    tools = [search, wiki_tool, arxiv_tool]
    search_agent = initialize_agent(tools, llm, agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,handling_parsing_errors=True)
    
    with st.chat_message("assistant"):
        st_cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)
        response = search_agent.run(st.session_state.messages, callbacks=[st_cb])
        st.session_state.messages.append({"role":"assisstant", "content":response})
        st.write(response)