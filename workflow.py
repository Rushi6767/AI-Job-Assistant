"""
LangGraph Workflow for Job Application Assistant Agent
This orchestrates all agents in a coordinated workflow
"""
from langgraph.graph import StateGraph, END
from state import ApplicationState
from agents.job_parser import parse_job_description
from agents.skills_analyzer import analyze_skills_gap
from agents.resume_optimizer import optimize_resume
from agents.cover_letter import generate_cover_letter
from agents.tracker import save_application


def create_workflow():
    """
    Create the LangGraph workflow that orchestrates all agents
    
    Workflow:
    1. Parse Job Description -> Extract requirements
    2. Analyze Skills Gap -> Compare resume with job
    3. Optimize Resume -> Tailor resume
    4. Generate Cover Letter -> Create personalized letter
    5. Save Application -> Store in tracking system
    """
    
    # Create the graph
    workflow = StateGraph(ApplicationState)
    
    # Add nodes (agents)
    workflow.add_node("parse_job", parse_job_description)
    workflow.add_node("analyze_skills", analyze_skills_gap)
    workflow.add_node("optimize_resume", optimize_resume)
    workflow.add_node("generate_cover_letter", generate_cover_letter)
    workflow.add_node("save_application", save_application)
    
    # Define the flow
    workflow.set_entry_point("parse_job")
    
    # Sequential flow
    workflow.add_edge("parse_job", "analyze_skills")
    workflow.add_edge("analyze_skills", "optimize_resume")
    workflow.add_edge("optimize_resume", "generate_cover_letter")
    workflow.add_edge("generate_cover_letter", "save_application")
    workflow.add_edge("save_application", END)
    
    # Compile the workflow
    app = workflow.compile()
    
    return app


def run_workflow(job_description: str, user_resume: str, 
                user_name: str = "Applicant", job_url: str = ""):
    """
    Run the complete workflow
    
    Args:
        job_description: The job posting text
        user_resume: The user's resume text
        user_name: User's name for cover letter
        job_url: Optional URL of the job posting
    
    Returns:
        Final state with all generated content
    """
    
    # Initialize state
    initial_state = {
        "job_description": job_description,
        "job_url": job_url,
        "user_resume": user_resume,
        "user_name": user_name,
        "user_email": None,
        "job_title": None,
        "company_name": None,
        "job_requirements": [],
        "job_skills": [],
        "tailored_resume": None,
        "cover_letter": None,
        "skills_gap": [],
        "match_score": None,
        "application_id": None,
        "application_status": "drafted",
        "messages": []
    }
    
    # Create and run workflow
    app = create_workflow()
    final_state = app.invoke(initial_state)
    
    return final_state


# For testing purposes
if __name__ == "__main__":
    # Test with dummy data
    test_job = """
    Senior Python Developer at TechCorp
    
    Requirements:
    - 5+ years Python experience
    - Experience with FastAPI and Django
    - Knowledge of Docker and Kubernetes
    - Strong problem-solving skills
    - Bachelor's degree in CS
    """
    
    test_resume = """
    John Doe
    Software Developer
    
    Experience:
    - 6 years of Python development
    - Built APIs using FastAPI
    - Worked with Docker containers
    - Strong analytical skills
    
    Education:
    Bachelor's in Computer Science
    """
    
    print("Running workflow test...")
    result = run_workflow(test_job, test_resume, "John Doe")
    print(f"\nJob: {result['job_title']} at {result['company_name']}")
    print(f"Match Score: {result['match_score']*100:.0f}%")
    print(f"Skills Gap: {result['skills_gap']}")
    print(f"Application ID: {result['application_id']}")

