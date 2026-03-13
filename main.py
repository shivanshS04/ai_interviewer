import streamlit as st
from app_pages import home, chat, summary
import time

def show_splash_screen():
    placeholder = st.empty()
    with placeholder.container():
        st.markdown("""
            <style>
            .splash-container {
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                height: 80vh;
                background: #000000;
                color: white;
                border-radius: 20px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.3);
                font-family: 'Inter', sans-serif;
            }
            .splash-title {
                font-size: 4rem;
                font-weight: 800;
                margin-bottom: 20px;
                text-align: center;
                animation: fadeInDown 1.5s ease-out;
            }
            .splash-subtitle {
                font-size: 1.5rem;
                opacity: 0.8;
                animation: fadeInUp 1.5s ease-out;
            }
            @keyframes fadeInDown {
                from { opacity: 0; transform: translateY(-30px); }
                to { opacity: 1; transform: translateY(0); }
            }
            @keyframes fadeInUp {
                from { opacity: 0; transform: translateY(30px); }
                to { opacity: 1; transform: translateY(0); }
            }
            </style>
            <div class="splash-container">
                <div class="splash-title">AI Technical Interviewer</div>
                <div class="splash-subtitle">Prepare for Success</div>
            </div>
        """, unsafe_allow_html=True)
    time.sleep(2)
    placeholder.empty()

def main():
    if "initialized" not in st.session_state:
        show_splash_screen()
        st.session_state.initialized = True

    if "page" not in st.session_state:
        st.session_state.page = "page1"

    if st.session_state.page == "page1":
        home.home()
    elif st.session_state.page == "page2":
        chat.chat()
    elif st.session_state.page == "page3":
        summary.summary()
    
if __name__ == "__main__":
    main()
