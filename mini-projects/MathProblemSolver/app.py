import streamlit as st
from langchain_groq import ChatGroq
from langchain.chains import LLMMathChain
from langchain.chains.llm import LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.agents.agent_types import AgentType
from langchain.agents import Tool, initialize_agent
from langchain.callbacks import StreamlitCallbackHandler


### Set up page config
st.set_page_config(page_title="Math Problem Solver and Data Search Assisstant")
st.title("Text to Math Problem Solver using Gemma 2")

groq_api_key = st.sidebar.text_input("Enter your Groq API Key:", type="password")


if not groq_api_key:
    st.info("Please add your Groq API Key to continue")
    st.stop()
    
    
engine = ChatGroq(groq_api_key=groq_api_key, model_name = "Gemma2-9b-It")



## Initialize Tools

wikipidea_wrapper = WikipediaAPIWrapper()
wiki_tool = Tool(
    name="Wikipidea",
    func=wikipidea_wrapper.run,
    description = "Tool for looking up Wikipedea."
)


math_chain = LLMMathChain.from_llm(llm=engine)

calculator = Tool(
    name="Calculator",
    func=math_chain.run,
    description="Tools for answering math question. Only input mathematical expressions"
)


prompt = """
You are an agent tasked with solving user's mathematical questions. Logically arrive at a solution and provide explanation and display it point wise for the following question: {question}. Answer :"""

prompt_template = PromptTemplate(
    input_variables=["question"],
    template=prompt
)


## Combining all tools into chain

chain1 = LLMChain(llm=engine, prompt=prompt_template)

resoning_tool = Tool(
    name="reasoning tool",
    func=chain1.run,
    description=" A tool for anaswering logic-based and reasoning questions"
)

assisstant_agent = initialize_agent(
    tools=[wiki_tool, calculator, resoning_tool],
    llm = engine,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=False,
    handle_parsing_errors=True
)

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {
            "role" : "assisstant",
            "content": "Hi, I'm a math chatbot, who can answer your questions"
        }
    ]
    
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])
    
    
def generate_response(question):
    response = assisstant_agent.invoke({"input": question})
    

question = st.text_area("Enter your question", placeholder="Whats 2 + 2 ?")
    
if st.button("Answer"):
    if question:
        with st.spinner("Generating response..."):
            st.session_state.messages.append({"role":"user", "content":question})
            
            st.chat_message("user").write(question)
            
            st_cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)
            response = assisstant_agent.run(st.session_state.messages, callbacks=[st_cb])
            
            st.session_state.messages.append({"role":"assisstant", "content":response})
            
            st.write("### Response:")
            st.success(response)
            
            
    else:
        st.warning("Please enter a Question")