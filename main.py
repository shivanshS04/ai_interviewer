import streamlit as st
from app_pages import home, chat

def main() :
    if "page" not in st.session_state:
        st.session_state.page = "page1"

    if st.session_state.page == "page1":
        home.home()
    elif st.session_state.page == "page2":
        chat.chat()
    
if __name__ == "__main__":
    main()
