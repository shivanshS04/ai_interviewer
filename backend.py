from typing import Annotated,Sequence,TypedDict
from langchain_ollama import ChatOllama
from langchain_core.messages import (
    AIMessage,
    HumanMessage,
    SystemMessage
)
from langgraph.graph import StateGraph, START,END

class ChatState(TypedDict):
    messages:Annotated[Sequence[HumanMessage|AIMessage|SystemMessage],'List of messages exchanged in the chat']

model= ChatOllama(model="llama3.2")

def initialize_chat(resume:str, job_role:str, experience:str, company_name:str, state:ChatState)->ChatState:
    system_prompt = SystemMessage(content =  f"""You are an AI interview assistant helping a user prepare for technical interviews.
The user has provided their resume and is targeting the role of {job_role} at {company_name} with {experience} experience.
RESUME CONTENT:
{resume}

Use the resume to generate relevant interview questions and provide feedback on the user's answers.
If the company name is provided, tailor your questions to the specific technologies and values associated with that company."""
    )
    
    # If this is the first message (empty conversation), add a prompt to start the interview
    messages_to_send = [system_prompt] + state['messages']
    if len(state['messages']) == 0:
        initial_prompt = HumanMessage(content="Please start the interview by asking me your first technical question based on my resume and the role I'm targeting.")
        messages_to_send.append(initial_prompt)
    
    response = model.invoke(messages_to_send)
    state['messages'].append(AIMessage(content=response.content))
    return state

graph = StateGraph(ChatState)
graph.add_node(initialize_chat, name="initialize_chat", inputs=["resume","job_role","experience","company_name","messages"], outputs=["messages"])
