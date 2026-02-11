import streamlit as st
import sys
import os
from utils.generate_audio import generate_audio
import asyncio
# Ensure root directory is in python path
sys.path.append(os.path.abspath('.'))
from backend import initialize_chat, ChatState, generate_performance_summary
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.messages import HumanMessage, AIMessage

from streamlit_monaco import st_monaco

from streamlit_mic_recorder import mic_recorder
from utils.transcribe import transcribe_audio

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
        st.divider()
        if st.button("End Session", use_container_width=True, type="secondary"):
            with st.spinner("Generating performance summary..."):
                # Prepare state for summary generation
                state = {
                    "messages": st.session_state.messages,
                    "feedbacks": st.session_state.feedbacks
                }
                summary = generate_performance_summary(state)
                st.session_state.performance_summary = summary
                st.session_state.page = "page3"
                st.rerun()

    st.title("Interview Session")
    
    # Ensure messages exist (fallback)
    if "messages" not in st.session_state:
        st.session_state.messages = []
        
    if "feedbacks" not in st.session_state:
        st.session_state.feedbacks = []
        
    if "current_question_type" not in st.session_state:
        st.session_state.current_question_type = "theory"

    if "input_id" not in st.session_state:
        st.session_state.input_id = 0

    # Display chat history
    for i, msg in enumerate(st.session_state.messages):
        if isinstance(msg, AIMessage):
            with st.chat_message("assistant"):
                if msg.content:
                    st.markdown(msg.content)
                    if msg.content.startswith("Question Type:"):
                         # This handles potential legacy content if any, but clean way:
                         pass 
                else:
                    st.warning("AI response was empty")
                
                # Check if this is the latest message to attach audio
                if i == len(st.session_state.messages) - 1:
                     if os.path.exists("speech.mp3"):
                         should_autoplay = st.session_state.get("autoplay_audio", False)
                         st.audio("speech.mp3", format="audio/mp3", autoplay=should_autoplay)
                         if should_autoplay:
                             st.session_state.autoplay_audio = False

        elif isinstance(msg, HumanMessage):
            with st.chat_message("user"):
                if msg.content:
                    st.markdown(msg.content)
                else:
                    st.warning("User message was empty")
                    
    # Input Area
    prompt = None
    question_type = st.session_state.get('current_question_type', 'theory')
    
    if question_type == 'coding':
        st.markdown("### Code Editor")
        
        languages = ["python", "javascript", "react", "java", "c", "cpp", "sql", "html", "css", "json"]
        selected_language = st.selectbox("Select Language", languages, index=0, key="editor_language")
        
        # Map specific selections to Monaco-supported languages
        # React is essentially JavaScript (JSX) in Monaco
        editor_lang_map = {
            "react": "javascript",
            "c": "c",
            "cpp": "cpp"
        }
        # Default to the selected language if not in map
        monaco_lang = editor_lang_map.get(selected_language, selected_language)
        
        # rudimentary comment mapping for default value if needed, 
        # but for now we keep the simple default or let user type.
        # Ideally we'd update 'value' only if it's empty or first load, 
        # but st_monaco might handle value updates differently.
        # We will just use the selected language for syntax highlighting.
        
        code_content = st_monaco(value="# Write your solution here\n", height="300px", language=monaco_lang)
        if st.button("Submit Solution", type="primary"):
            prompt = code_content
    else:
        # Standard Layout: Voice Recorder + Text Input
        st.write("### Answer the Question")
        
        # Voice Input
        st.write("🎙️ **Voice Answer:**")
        audio = mic_recorder(start_prompt="Start Recording", stop_prompt="Stop Recording", key=f'recorder_{st.session_state.input_id}')
            
        # Text Input
        text_input = st.chat_input("Or type your answer here...", key="chat_input")

        # Handle Audio Input
        if audio:
            st.spinner("Transcribing audio...")
            transcribed_text = transcribe_audio(audio['bytes'])
            if transcribed_text:
                prompt = transcribed_text
        elif text_input:
            prompt = text_input
        
        
    # Process Input
    if prompt:
        # Add user message
        # If coding, format as markdown code block for history
        if question_type == 'coding':
            # Use the selected language for markdown formatting if available, else default to python
            lang_for_md = st.session_state.get("editor_language", "python")
            display_content = f"```{lang_for_md}\n{prompt}\n```"
            st.session_state.messages.append(HumanMessage(content=display_content))
            with st.chat_message("user"):
                st.markdown(display_content)
        else:
            st.session_state.messages.append(HumanMessage(content=prompt))
            with st.chat_message("user"):
                st.markdown(prompt)
        prompt = None  # Reset prompt after processing
                
        # Get AI response
        try:
            with st.spinner("Interviewer is thinking..."):
                # ... (State preparation) ...
                state = {
                    "messages": st.session_state.messages,
                    "feedbacks": st.session_state.feedbacks
                }
                
                new_state = initialize_chat(resume, job_role, experience, company_name, state)
                
                # Update session state
                st.session_state.messages = new_state['messages']
                if 'feedbacks' in new_state:
                    st.session_state.feedbacks = new_state['feedbacks']
                
                # Get the latest message content (which is now just the question)
                latest_response = st.session_state.messages[-1].content
                
                # Get question type if available
                new_question_type = new_state.get('current_question_type', 'theory')
                st.session_state.current_question_type = new_question_type
                
                # Audio generation is now handled in backend.py
                # asyncio.run(generate_audio(latest_response)) 
                
                # Trigger autoplay for next run
                st.session_state.autoplay_audio = True
                
                # Increment input_id to reset the recorder
                st.session_state.input_id += 1
                
                # Rerun to update UI
                st.rerun()
                
        except Exception as e:
            st.error(f"Error generating response: {e}")