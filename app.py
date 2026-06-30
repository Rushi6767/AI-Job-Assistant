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
    user_name = st.text_input("Your Name", value="Rushi Sathavara")
    
    # Resume input options
    resume_option = st.radio(
        "Choose resume input method:",
        ["Upload File (PDF/DOCX/TXT)", "Paste Text"]
    )
    
    user_resume = ""
    
    if resume_option == "Upload File (PDF/DOCX/TXT)":
        uploaded_file = st.file_uploader(
            "Upload Your Resume (PDF or TXT)",
            type=['pdf', 'docx', 'txt'],
            help="Upload your resume in PDF, DOCX, or TXT format"
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
            "Paste Job Description",
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
            st.metric("Recommendation", result.get('recommendation', 'N/A'))
        
        # Tabs for outputs
        output_tab1, output_tab2, output_tab3 = st.tabs(["📋 Quick Check", "📄 LaTeX Resume", "📝 Cover Letter"])
        
        with output_tab1:
            st.subheader("Suitability Quick Check")
            st.info(result.get('quick_check_result', 'No quick check result available.'))
            
            recommendation = result.get('recommendation', '').upper()
            if recommendation == "SKIP":
                st.error("⛔ Skipping resume generation — role has disqualifying requirements.")
        
        with output_tab2:
            st.subheader("LaTeX Resume")
            recommendation = result.get('recommendation', '').upper()
            if recommendation == "SKIP":
                st.warning("⚠️ No LaTeX resume generated due to SKIP recommendation.")
            else:
                latex_output = result.get('latex_resume', '')
                st.code(latex_output, language="latex")
                
                # Dynamic filename extraction
                company_fn = result.get('company_name') or 'Company'
                role_fn = result.get('job_title') or 'Role'
                import re
                company_clean = re.sub(r'[^a-zA-Z0-9]', '_', company_fn).strip('_')
                role_clean = re.sub(r'[^a-zA-Z0-9]', '_', role_fn).strip('_')
                filename = f"Rushi_Sathavara_{company_clean}_{role_clean}.tex"
                if not company_clean or not role_clean:
                    filename = "Rushi_Sathavara_Resume.tex"
                
                # Download button
                st.download_button(
                    label="⬇️ Download .tex file",
                    data=latex_output,
                    file_name=filename,
                    mime="text/plain"
                )
                
                # Overleaf integration button
                import base64
                import urllib.parse
                encoded_tex = base64.b64encode(latex_output.encode('utf-8')).decode('utf-8')
                overleaf_url = f"https://www.overleaf.com/docs?snip_uri=data:application/x-tex;base64,{encoded_tex}"
                st.link_button("🚀 Open in Overleaf", overleaf_url)
                
                # ATS Score details
                st.divider()
                st.subheader("ATS Score Details")
                
                ats_score_dict = result.get('ats_score', {})
                score = ats_score_dict.get('score', 0)
                if not score and result.get('match_score') is not None:
                    score = int(result['match_score'] * 100)
                
                st.metric("ATS Match Score", f"{score}/100")
                
                col_match, col_miss = st.columns(2)
                with col_match:
                    st.markdown("**Matched keywords:**")
                    matched_kws = result.get('matched_keywords', [])
                    if matched_kws:
                        for kw in matched_kws:
                            st.markdown(f"- ✅ {kw}")
                    else:
                        st.markdown("- None detected")
                with col_miss:
                    st.markdown("**Missing keywords:**")
                    missing_kws = result.get('missing_keywords', [])
                    if missing_kws:
                        for kw in missing_kws:
                            st.markdown(f"- ⚠️ {kw}")
                    else:
                        st.success("✅ No missing keywords detected!")
                        
                # Skills gap summary
                if matched_kws or missing_kws:
                    total_kws = len(matched_kws) + len(missing_kws)
                    missing_str = ", ".join(missing_kws[:5])
                    st.markdown(f"**Skills Gap Summary:** You match {len(matched_kws)}/{total_kws} keywords. Missing: {missing_str}. Consider adding these to your profile if you have relevant experience.")
        
        with output_tab3:
            st.subheader("Cover Letter")
            recommendation = result.get('recommendation', '').upper()
            if recommendation == "SKIP":
                st.warning("⚠️ No cover letter generated due to SKIP recommendation.")
            else:
                cover_letter = result.get('cover_letter', '')
                st.text_area("", value=cover_letter, height=400, key="cover_letter_output")
                st.download_button(
                    "📥 Download Cover Letter",
                    cover_letter,
                    file_name=f"cover_letter_{result.get('company_name', 'company')}_{datetime.now().strftime('%Y%m%d')}.txt",
                    mime="text/plain"
                )

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

