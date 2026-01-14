import streamlit as st




def initiallize_ai(resume, job_role, experience):
    toaster = st.toast("Initializing AI...")
    if resume is None:
        toaster.toast("Please upload your resume.",icon="⚠️",duration="short")
        return 
    if job_role.strip() == "":
        toaster.toast("Please enter the job role you are targeting.",icon="⚠️",duration="short")
        return
    if experience.strip() == "":
        experience = 'Fresher'
    
    toaster.toast("Uploading resume...",icon="⏳")
    toaster.toast("AI Initialized successfully!",icon="✅",duration="short")

def main() :
    st.title("🧩 Technical Interview Prep")
    with st.form("initialize_ai_form"):

        resume = st.file_uploader("Upload your resume", type=["pdf"],accept_multiple_files=False)
        job_role = st.text_input("What job role are you targeting?")
        experience = st.selectbox("what is your experience level?",['Fresher','Entry-level','Mid-level','Senior-level'])
        submit_btn = st.form_submit_button("Generate Interview Questions",shortcut="ctrl+enter",width="stretch")
        if submit_btn:
            initiallize_ai(resume, job_role, experience)
if __name__ == "__main__":
    main()
