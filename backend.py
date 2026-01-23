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

def initialize_chat(resume:str, job_role:str, experience:str , state:ChatState)->ChatState:
    system_prompt = SystemMessage(content =  f"""You are an AI interview assistant helping a user prepare for technical interviews.
The user has provided their resume and is targeting the role of {job_role} with {experience} experience.
Use the resume to generate relevant interview questions and provide feedback on the user's answers."""
    )

    response = model.invoke([system_prompt]+state['messages'])
    state['messages'].append(AIMessage(content=response.content))
    return state

graph = StateGraph(ChatState)
graph.add_node(initialize_chat, name="initialize_chat", inputs=["resume","job_role","experience","messages"], outputs=["messages"])
