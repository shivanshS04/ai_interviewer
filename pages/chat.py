import streamlit as st

def handle_back():
    st.session_state.page = "page1"
def chat():
    st.button("Back",on_click=handle_back, icon="⬅️",use_container_width=False)
    st.title("💬 Interview interface")
    st.chat_input("Type your questions here...",key="chat_input")