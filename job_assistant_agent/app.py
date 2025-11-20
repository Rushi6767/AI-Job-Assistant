"""
Streamlit UI for Job Application Assistant Agent
"""
import streamlit as st
from workflow import run_workflow
from agents.tracker import load_applications, update_application_status
from tools.pdf_parser import parse_resume
import os
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Job Application Assistant",
    page_icon="💼",
    layout="wide"
)

# Title and description
st.title("💼 Job Application Assistant Agent")
st.markdown("""
This AI agent helps you tailor your resume and generate cover letters for job applications.
Upload your resume, paste a job description, and let the agent optimize your application!
""")

# Sidebar for resume upload
with st.sidebar:
    st.header("📄 Your Resume")
    
    # Name input
    user_name = st.text_input("Your Name", value="John Doe")
    
    # Resume input options
    resume_option = st.radio(
        "Choose resume input method:",
        ["Upload File (PDF/DOCX)", "Paste Text"]
    )
    
    user_resume = ""
    
    if resume_option == "Upload File (PDF/DOCX)":
        uploaded_file = st.file_uploader(
            "Upload your resume",
            type=['pdf', 'docx'],
            help="Upload your resume in PDF or DOCX format"
        )
        
        if uploaded_file:
            # Save temporarily
            temp_path = f"data/resumes/temp_{uploaded_file.name}"
            os.makedirs("data/resumes", exist_ok=True)
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            # Parse the file
            user_resume = parse_resume(temp_path)
            st.success("✅ Resume uploaded and parsed!")
            
            # Show preview
            with st.expander("Preview Resume"):
                st.text(user_resume[:500] + "..." if len(user_resume) > 500 else user_resume)
    
    else:
        user_resume = st.text_area(
            "Paste your resume here",
            height=300,
            placeholder="Paste your resume text here..."
        )

# Main content area
tab1, tab2, tab3 = st.tabs(["🎯 New Application", "📊 Application Tracker", "ℹ️ About"])

# Tab 1: New Application
with tab1:
    st.header("Create New Application")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        job_url = st.text_input(
            "Job URL (optional)",
            placeholder="https://company.com/careers/job-id"
        )
        
        job_description = st.text_area(
            "Job Description",
            height=300,
            placeholder="Paste the job description here...",
            help="Copy and paste the full job posting"
        )
    
    with col2:
        st.markdown("### 🚀 Quick Tips")
        st.info("""
        **For best results:**
        1. Include complete job description
        2. Make sure your resume has relevant experience
        3. Review and customize the generated content
        4. Use keywords from the job posting
        """)
    
    # Generate button
    if st.button("🎨 Generate Application Materials", type="primary", use_container_width=True):
        
        # Validation
        if not user_resume:
            st.error("⚠️ Please provide your resume first!")
        elif not job_description:
            st.error("⚠️ Please provide a job description!")
        else:
            # Run the workflow
            with st.spinner("🤖 AI Agent is working... This may take 30-60 seconds..."):
                try:
                    result = run_workflow(
                        job_description=job_description,
                        user_resume=user_resume,
                        user_name=user_name,
                        job_url=job_url
                    )
                    
                    # Store result in session state
                    st.session_state['last_result'] = result
                    st.success("✅ Application materials generated successfully!")
                    
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
                    st.exception(e)
    
    # Display results
    if 'last_result' in st.session_state:
        result = st.session_state['last_result']
        
        st.divider()
        st.header("📋 Results")
        
        # Job info
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Job Title", result.get('job_title', 'N/A'))
        with col2:
            st.metric("Company", result.get('company_name', 'N/A'))
        with col3:
            match_score = result.get('match_score', 0) * 100
            st.metric("Match Score", f"{match_score:.0f}%")
        
        # Skills gap
        if result.get('skills_gap'):
            st.warning(f"**Skills to Highlight:** {', '.join(result['skills_gap'][:5])}")
        
        # Tabs for outputs
        output_tab1, output_tab2, output_tab3 = st.tabs(["📝 Tailored Resume", "✉️ Cover Letter", "🔍 Skills Analysis"])
        
        with output_tab1:
            st.subheader("Tailored Resume")
            tailored_resume = result.get('tailored_resume', '')
            st.text_area("", value=tailored_resume, height=400, key="resume_output")
            st.download_button(
                "📥 Download Resume",
                tailored_resume,
                file_name=f"resume_{result.get('company_name', 'company')}_{datetime.now().strftime('%Y%m%d')}.txt",
                mime="text/plain"
            )
        
        with output_tab2:
            st.subheader("Cover Letter")
            cover_letter = result.get('cover_letter', '')
            st.text_area("", value=cover_letter, height=400, key="cover_letter_output")
            st.download_button(
                "📥 Download Cover Letter",
                cover_letter,
                file_name=f"cover_letter_{result.get('company_name', 'company')}_{datetime.now().strftime('%Y%m%d')}.txt",
                mime="text/plain"
            )
        
        with output_tab3:
            st.subheader("Skills Analysis")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Required Skills:**")
                for skill in result.get('job_skills', [])[:10]:
                    st.markdown(f"- {skill}")
            
            with col2:
                st.markdown("**Skills Gap:**")
                skills_gap = result.get('skills_gap', [])
                if skills_gap:
                    for skill in skills_gap[:10]:
                        st.markdown(f"- ⚠️ {skill}")
                else:
                    st.success("✅ Great match! No major skills gaps detected.")

# Tab 2: Application Tracker
with tab2:
    st.header("Application Tracker")
    
    applications = load_applications()
    
    if not applications:
        st.info("📭 No applications tracked yet. Create your first application in the 'New Application' tab!")
    else:
        st.success(f"📊 Total Applications: {len(applications)}")
        
        # Display applications in a table
        for app in reversed(applications):  # Show newest first
            with st.expander(f"🏢 {app.get('job_title', 'Unknown')} at {app.get('company', 'Unknown')} - {app.get('status', 'N/A')}"):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown(f"**Application ID:** {app.get('id', 'N/A')}")
                    st.markdown(f"**Date:** {app.get('date_created', 'N/A')[:10]}")
                
                with col2:
                    st.markdown(f"**Match Score:** {app.get('match_score', 0)*100:.0f}%")
                    st.markdown(f"**Status:** {app.get('status', 'N/A')}")
                
                with col3:
                    st.markdown(f"**Resume:** {'✅' if app.get('has_tailored_resume') else '❌'}")
                    st.markdown(f"**Cover Letter:** {'✅' if app.get('has_cover_letter') else '❌'}")
                
                # Status update
                new_status = st.selectbox(
                    "Update Status",
                    ["drafted", "applied", "interview", "rejected", "accepted"],
                    index=["drafted", "applied", "interview", "rejected", "accepted"].index(app.get('status', 'drafted')),
                    key=f"status_{app['id']}"
                )
                
                if st.button(f"Update", key=f"btn_{app['id']}"):
                    update_application_status(app['id'], new_status)
                    st.success("Status updated!")
                    st.rerun()

# Tab 3: About
with tab3:
    st.header("About This Agent")
    
    st.markdown("""
    ### 🤖 How It Works
    
    This Job Application Assistant uses **LangGraph** to orchestrate multiple AI agents:
    
    1. **Job Parser Agent** - Extracts key information from job descriptions
    2. **Skills Analyzer Agent** - Compares your skills with job requirements
    3. **Resume Optimizer Agent** - Tailors your resume using RAG (Retrieval-Augmented Generation)
    4. **Cover Letter Agent** - Generates personalized cover letters
    5. **Tracker Agent** - Manages your application pipeline
    
    ### 🛠️ Tech Stack
    
    - **LangGraph**: Agent orchestration and workflow management
    - **OpenAI GPT-4**: Language model for generation
    - **ChromaDB**: Vector database for RAG
    - **Streamlit**: User interface
    - **Python**: Core implementation
    
    ### 🎯 Design Pattern
    
    This agent follows the **Multi-Agent Orchestration** pattern with:
    - Sequential workflow for predictable results
    - State management across agents
    - RAG for learning from past applications
    - Persistent storage for application tracking
    
    ### 📝 Best Practices
    
    - Always review and customize generated content
    - Keep your resume updated
    - Track all applications for better insights
    - Use specific job descriptions for best results
    
    ---
    
    **Built for CISC691 - Agentic AI**
    
    Assignment 03: Building the AI Agent of Your Choice
    """)

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: gray;'>
    <p>💼 Job Application Assistant Agent | Powered by LangGraph & OpenAI GPT-4</p>
</div>
""", unsafe_allow_html=True)

