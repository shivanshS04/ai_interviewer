import streamlit as st

def initialize_chat(resume, job_role, experience):
    

def handle_back():
    st.session_state.page = "page1"
def chat(resume, job_role, experience):
    initialize_chat(resume, job_role, experience)
    st.button("Back",on_click=handle_back, icon="⬅️",use_container_width=False)
    st.title("💬 Interview interface")
    st.chat_input("Type your questions here...",key="chat_input")