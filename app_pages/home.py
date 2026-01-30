import streamlit as st
import pypdf
import time
import sys
import os

# Ensure root directory is in python path to import backend
sys.path.append(os.path.abspath('.'))
from backend import initialize_chat

def initiallize_ai(resume, job_role, experience, company_name):
    with st.status("Initializing AI Interviewer...", expanded=True) as status:
        if resume is None:
            status.update(label="Error: Resume missing", state="error", expanded=False)
            st.error("Please upload your resume to proceed.")
            return 
        if job_role.strip() == "":
            status.update(label="Error: Job role missing", state="error", expanded=False)
            st.error("Please enter the job role you are targeting.")
            return
        if experience.strip() == "":
            experience = 'Fresher'
        
        st.write("Processing resume and analyzing profile...")
        # Extract text from PDF
        try:
            pdf_reader = pypdf.PdfReader(resume)
            resume_text = ""
            for page in pdf_reader.pages:
                resume_text += page.extract_text()
            time.sleep(1) # Simulate processing for better UX
        except Exception as e:
            status.update(label="Error processing PDF", state="error")
            st.error(f"Error reading PDF: {e}")
            return

        st.write("Generating first interview question...")
        try:
            # Pre-generate the first question here so it's ready for the chat page
            state = {"messages": []}
            new_state = initialize_chat(resume_text, job_role, experience, company_name, state)
            generated_messages = new_state['messages']
        except Exception as e:
             status.update(label="AI Generation Error", state="error")
             st.error(f"Failed to generate opening question: {e}")
             return

        status.update(label="AI Initialized successfully!", state="complete", expanded=False)
    
    # CRITICAL: Store ALL session state OUTSIDE the status context and BEFORE rerun
    st.session_state.messages = generated_messages
    st.session_state.page = "page2"
    st.session_state.resume = resume_text
    st.session_state.job_role = job_role
    st.session_state.experience = experience
    st.session_state.company_name = company_name
    
    # Slight delay to show success state before rerunning
    time.sleep(0.5)
    st.rerun()

def home():
    st.title("AI Technical Interviewer")
    st.markdown("""
    Welcome to the AI Technical Interviewer. This tool helps you prepare for your technical interviews by simulating a real interview experience based on your resume and target role.
    
    Please provide your details below to start the session.
    """)
    
    st.divider()
    
    with st.form("initialize_ai_form", enter_to_submit=False, border=True):
        st.subheader("Candidate Details")
        
        col1, col2 = st.columns(2)
        
        with col1:
            job_role = st.text_input("Target Job Role", placeholder="e.g. Software Engineer, Data Scientist")
        
        with col2:
            experience = st.selectbox("Experience Level", ['Fresher', 'Entry-level', 'Mid-level', 'Senior-level'])
            
        company_name = st.text_input("Target Company (Optional)", placeholder="e.g. Google, Microsoft, Startup")
        
        resume = st.file_uploader("Upload Resume (PDF)", type=["pdf"], accept_multiple_files=False)
        st.caption("Your resume will be analyzed to generate relevant interview questions.")

        st.markdown("<br>", unsafe_allow_html=True)
        
        submit_btn = st.form_submit_button("Start Interview Session", use_container_width=True, type="primary")
        
        if submit_btn:
            initiallize_ai(resume, job_role, experience, company_name)