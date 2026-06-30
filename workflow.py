"""
LangGraph Workflow for Job Application Assistant Agent
This orchestrates all agents in a coordinated workflow
"""
from langgraph.graph import StateGraph, END
from state import GraphState
from agents.quick_check import quick_check_agent
from agents.resume_latex import resume_latex_agent
from agents.cover_letter import generate_cover_letter
from agents.ats_scorer import ats_score_agent


def create_workflow():
    """
    Create the LangGraph workflow that orchestrates all agents
    
    Workflow:
    1. Quick Suitability Check -> Evaluate JD background & hard blockers
    2. Route Conditional -> SKIP stops workflow, APPLY/MAYBE continues
    3. Generate LaTeX Resume -> Tailor Rushi's details into compilable LaTeX
    4. Generate Cover Letter -> Create personalized letter
    5. ATS Match Score -> Calculate keyword matches and save application
    """
    
    # Create the graph
    workflow = StateGraph(GraphState)
    
    # Add nodes (agents)
    workflow.add_node("quick_check", quick_check_agent)
    workflow.add_node("resume_latex", resume_latex_agent)
    workflow.add_node("generate_cover_letter", generate_cover_letter)
    workflow.add_node("ats_score", ats_score_agent)
    
    # Define the flow
    workflow.set_entry_point("quick_check")
    
    # Conditional routing
    def should_continue(state: GraphState):
        recommendation = state.get("recommendation", "MAYBE").upper()
        if recommendation == "SKIP":
            return "end"
        else:
            return "continue"
            
    workflow.add_conditional_edges(
        "quick_check",
        should_continue,
        {
            "end": END,
            "continue": "resume_latex"
        }
    )
    
    # Remaining steps
    workflow.add_edge("resume_latex", "generate_cover_letter")
    workflow.add_edge("generate_cover_letter", "ats_score")
    workflow.add_edge("ats_score", END)
    
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
        # Inputs
        "jd_text": job_description,
        "resume_text": user_resume,
        "job_description": job_description,  # compatibility
        "user_resume": user_resume,          # compatibility
        "job_url": job_url,
        "user_name": user_name,
        "user_email": None,
        
        # Parsed job info
        "job_title": None,
        "company_name": None,
        "job_requirements": [],
        "job_skills": [],
        
        # Outputs
        "quick_check_result": "",
        "recommendation": "",
        "latex_resume": "",
        "tailored_resume": None,
        "cover_letter": None,
        "skills_gap": [],
        "match_score": None,
        "ats_score": {},
        "matched_keywords": [],
        "missing_keywords": [],
        
        # Tracking
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

