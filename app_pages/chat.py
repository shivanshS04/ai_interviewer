import streamlit as st
import sys
import os
# Ensure root directory is in python path
sys.path.append(os.path.abspath('.'))
from backend import initialize_chat, ChatState
from langchain_core.messages import HumanMessage, AIMessage

def handle_back():
    st.session_state.page = "page1"

def chat():
    # Retrieve data from session state
    resume = st.session_state.get('resume')
    job_role = st.session_state.get('job_role')
    experience = st.session_state.get('experience')
    company_name = st.session_state.get('company_name', "target company")
    
    # Sidebar for session context
    with st.sidebar:
        st.header("Session Details")
        st.markdown(f"**Role:** {job_role}")
        st.markdown(f"**Experience:** {experience}")
        if company_name:
            st.markdown(f"**Target Company:** {company_name}")
        
        st.divider()
        st.button("End Session", on_click=handle_back, use_container_width=True, type="secondary")

    st.title("Interview Session")
    
    # Ensure messages exist (fallback)
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for msg in st.session_state.messages:
        if isinstance(msg, AIMessage):
            with st.chat_message("assistant"):
                if msg.content:
                    st.markdown(msg.content)
                else:
                    st.warning("AI response was empty")
        elif isinstance(msg, HumanMessage):
            with st.chat_message("user"):
                if msg.content:
                    st.markdown(msg.content)
                else:
                    st.warning("User message was empty")

    # Chat input
    if prompt := st.chat_input("Type your answer here...", key="chat_input"):
        # Add user message
        st.session_state.messages.append(HumanMessage(content=prompt))
        with st.chat_message("user"):
            st.write(prompt)
            
        # Get AI response
        try:
            with st.spinner("Interviewer is thinking..."):
                state = {"messages": st.session_state.messages}
                new_state = initialize_chat(resume, job_role, experience, company_name, state)
                st.session_state.messages = new_state['messages']
                # Display new AI message
                with st.chat_message("assistant"):
                    st.write(st.session_state.messages[-1].content)
        except Exception as e:
            st.error(f"Error generating response: {e}")