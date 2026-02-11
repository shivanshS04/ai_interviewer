from typing import Annotated, Sequence, TypedDict, List, Literal
# from langchain_ollama import ChatOllama
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import (
    AIMessage,
    HumanMessage,
    SystemMessage
)
from langgraph.graph import StateGraph, START, END
from pydantic import BaseModel, Field
from utils.generate_audio import generate_audio
import asyncio
from dotenv import load_dotenv
import os
load_dotenv()

class InterviewResponse(BaseModel):
    question: str = Field(description="The interview question to ask the candidate.")
    feedback: str = Field(description="Feedback on the candidate's previous answer. If this is the first question, provide a welcoming opening.")
    type: Literal['theory', 'coding'] = Field(description="The type of the question, MUST be either 'theory' or 'coding'. Theory questions require user to write an answer whereas coding question requires user to submit the relevant code")

class ChatState(TypedDict):
    messages: Annotated[Sequence[HumanMessage | AIMessage | SystemMessage], 'List of messages exchanged in the chat']
    feedbacks: Annotated[List[str], 'List of feedbacks provided by the AI']

# model = ChatOllama(model="llama3.2")
model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash"
)

def initialize_chat(resume: str, job_role: str, experience: str, company_name: str, state: ChatState) -> ChatState:
    system_prompt = SystemMessage(content=f"""You are an AI interview assistant helping a user prepare for technical interviews.
The user has provided their resume and is targeting the role of {job_role} at {company_name} with {experience} experience.
RESUME CONTENT:
{resume}

Use the resume to generate relevant interview questions and provide feedback on the user's answers.
If the company name is provided, tailor your questions to the specific technologies and values associated with that company.

IMPORTANT: You must balance the interview with both 'theory' and 'coding' questions. 
Do not ask consecutive coding questions unless the user failed the previous one. 
Aim for a mix of conceptual understanding and practical coding skills."""
    )
    
    # If this is the first message (empty conversation), add a prompt to start the interview
    messages_to_send = [system_prompt] + state['messages']
    if len(state['messages']) == 0:
        initial_prompt = HumanMessage(content="Please start the interview by asking me your first technical question based on my resume and the role I'm targeting.")
        messages_to_send.append(initial_prompt)
    
    # Use structured output
    structured_model = model.with_structured_output(InterviewResponse)
    response = structured_model.invoke(messages_to_send)
    
    # Debugging: Print response type and content
    print(f"DEBUG: Response Type: {type(response)}")
    print(f"DEBUG: Response Content: {response}")
    
    # Update state
    # We append the QUESTION ONLY to the messages history so the conversation flow remains natural
    # Ensure content is string
    question_content = response.question
    if not isinstance(question_content, str):
        question_content = str(question_content)
        
    state['messages'].append(AIMessage(content=question_content))
    asyncio.run(generate_audio(response.question))
    # Initialize feedbacks list if not present
    if 'feedbacks' not in state:
        state['feedbacks'] = []
        
    state['feedbacks'].append(response.feedback)
    
    # We can also store the type in the state if needed, but the requirement was mainly to send it back. 
    # Since we return the whole state, we can add it as a temporary field or just rely on the frontend 
    # to handle the structured response if we returned it directly. 
    # However, since we are bound by ChatState, let's add a 'current_question_type' field to ChatState.
    state['current_question_type'] = response.type
    
    return state

# Update ChatState definition to include the new field
class ChatState(TypedDict):
    messages: Annotated[Sequence[HumanMessage | AIMessage | SystemMessage], 'List of messages exchanged in the chat']
    feedbacks: Annotated[List[str], 'List of feedbacks provided by the AI']
    current_question_type: Annotated[str, 'Type of the current question']

graph = StateGraph(ChatState)
graph.add_node("initialize_chat", initialize_chat) # Using string name for node is cleaner
