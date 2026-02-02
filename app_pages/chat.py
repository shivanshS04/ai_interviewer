import streamlit as st
import streamlit.components.v1 as components
import sys
import os
# Ensure root directory is in python path
sys.path.append(os.path.abspath('.'))
from backend import initialize_chat, ChatState
from langchain_core.messages import HumanMessage, AIMessage
from app_pages.speech_component import speech_to_text_component, text_to_speech_component

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
        
        # Speech speed control
        st.subheader("Speech Settings")
        speech_speed = st.slider(
            "AI Voice Speed",
            min_value=0.5,
            max_value=2.0,
            value=1.3,
            step=0.1,
            help="Adjust how fast the AI speaks (1.0 = normal)"
        )
        st.session_state.speech_speed = speech_speed
        
        st.divider()
        st.button("End Session", on_click=handle_back, use_container_width=True, type="secondary")

    st.title("Interview Session")
    
    # Ensure messages exist (fallback)
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    speech_speed = st.session_state.get('speech_speed', 1.3)
    for i, msg in enumerate(st.session_state.messages):
        if isinstance(msg, AIMessage):
            with st.chat_message("assistant"):
                if msg.content:
                    st.markdown(msg.content)
                    # Auto-play TTS for the last AI message only
                    if i == len(st.session_state.messages) - 1:
                        text_to_speech_component(msg.content, speed=speech_speed)
                else:
                    st.warning("AI response was empty")
        elif isinstance(msg, HumanMessage):
            with st.chat_message("user"):
                if msg.content:
                    st.markdown(msg.content)
                else:
                    st.warning("User message was empty")
    
    # Voice input section
    st.markdown("---")
    st.markdown("**Your Response**")
    
    use_voice = st.checkbox("Use Voice Input", help="Enable microphone to speak your answer")
    
    if use_voice:
        st.info("**Instructions:** \n1. Click the microphone button\n2. Allow microphone access if prompted\n3. Speak your answer (appears in gray box below)\n4. Click pause when done\n5. **Type or paste the text** from the gray box into the text area\n6. Click 'Send Answer'")
        
        # Speech component
        speech_to_text_component(key="voice_input")
        
        # Initialize voice transcript
        if 'voice_transcript' not in st.session_state:
            st.session_state.voice_transcript = ""
        
        # Text area to type/paste transcription
        voice_text = st.text_area(
            "Your answer (type or paste from above):",
            value=st.session_state.voice_transcript,
            height=100,
            key="voice_text_area",
            placeholder="Type or paste your answer here..."
        )
        
        # Send and Clear buttons
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("Send Answer", type="primary", use_container_width=True, key="send_voice"):
                if voice_text and voice_text.strip():
                    st.session_state.pending_message = voice_text.strip()
                    st.session_state.voice_transcript = ""
                    st.rerun()
                else:
                    st.warning("Please enter your answer first!")
        with col2:
            if st.button("Clear", use_container_width=True, key="clear_voice"):
                st.session_state.voice_transcript = ""
                st.rerun()
    
    # Regular text input
    prompt = st.chat_input("Type your answer here or use the Voice Input option above...", key="chat_input")
    
    # Check for pending message from voice input
    if st.session_state.get('pending_message'):
        prompt = st.session_state.pending_message
        st.session_state.pending_message = None
    
    if prompt and isinstance(prompt, str):
        # Add user message
        st.session_state.messages.append(HumanMessage(content=prompt))
        with st.chat_message("user"):
            st.markdown(prompt)
            
        # Get AI response
        try:
            with st.spinner("Interviewer is thinking..."):
                state = {"messages": st.session_state.messages}
                new_state = initialize_chat(resume, job_role, experience, company_name, state)
                st.session_state.messages = new_state['messages']
                # Display new AI message
                with st.chat_message("assistant"):
                    ai_response = st.session_state.messages[-1].content
                    st.markdown(ai_response)
                    # Speak the AI response
                    text_to_speech_component(ai_response, speed=speech_speed)
        except Exception as e:
            st.error(f"Error generating response: {e}")
        
        st.rerun()