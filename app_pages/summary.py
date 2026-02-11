import streamlit as st
import plotly.graph_objects as go
from backend import PerformanceSummary

def summary():
    st.title("Interview Performance Summary")
    
    if "performance_summary" not in st.session_state or not st.session_state.performance_summary:
        st.warning("No performance summary available. Please complete an interview session first.")
        if st.button("Go Home"):
            st.session_state.page = "page1"
            st.rerun()
        return

    summary_data: PerformanceSummary = st.session_state.performance_summary
    
    # --- Overall Score Gauge ---
    fig_gauge = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = summary_data.overall_score,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Overall Score"},
        gauge = {
            'axis': {'range': [0, 10]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 4], 'color': "lightcoral"},
                {'range': [4, 7], 'color': "lightyellow"},
                {'range': [7, 10], 'color': "lightgreen"}
            ],
        }
    ))
    st.plotly_chart(fig_gauge, use_container_width=True)
    
    # --- Radar Chart ---
    categories = ['Technical Accuracy', 'Communication', 'Problem Solving', 'Code Quality']
    scores = [
        summary_data.technical_accuracy, 
        summary_data.communication_skills, 
        summary_data.problem_solving, 
        summary_data.code_quality
    ]
    
    fig_radar = go.Figure(data=go.Scatterpolar(
        r=scores,
        theta=categories,
        fill='toself'
    ))

    fig_radar.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 10]
            )),
        showlegend=False,
        title="Skill Breakdown"
    )
    st.plotly_chart(fig_radar, use_container_width=True)
    
    # --- Textual Feedback ---
    st.divider()
    # --- Textual Feedback ---
    st.divider()
    st.subheader("Performance Analysis")
    st.info(f"**Executive Summary:**\n\n{summary_data.summary_text}")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.success("**✅ Strengths**")
        for item in summary_data.strengths:
            st.write(f"• {item}")
            
    with col2:
        st.warning("**🚀 Areas for Improvement**")
        for item in summary_data.improvement_areas:
            st.write(f"• {item}")
            
    if summary_data.weaknesses and summary_data.weaknesses[0] != "N/A":
        st.error("**🔍 Weaknesses to Address**")
        for item in summary_data.weaknesses:
            st.write(f"• {item}")
        
    st.divider()
    if st.button("Start New Session", type="primary"):
        # Reset session state
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.session_state.page = "page1"
        st.rerun()
