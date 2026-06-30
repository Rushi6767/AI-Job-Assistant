"""
State definition for the Job Application Assistant Agent
"""
from typing import TypedDict, List, Optional, Annotated
from langgraph.graph import add_messages


class GraphState(TypedDict):
    """State object that flows through the agent workflow"""
    
    # Input
    job_url: Optional[str]
    job_description: str
    user_resume: str
    user_name: Optional[str]
    user_email: Optional[str]
    
    # New input key names for GraphState mapping
    jd_text: str
    resume_text: str
    
    # Parsed job information
    job_title: Optional[str]
    company_name: Optional[str]
    job_requirements: List[str]
    job_skills: List[str]
    
    # Generated outputs
    tailored_resume: Optional[str]
    cover_letter: Optional[str]
    skills_gap: List[str]
    match_score: Optional[float]
    
    # New outputs for latex/quick check/ats scoring
    quick_check_result: str        # 5-line string
    recommendation: str            # "APPLY" / "SKIP" / "MAYBE"
    latex_resume: str              # full .tex string
    ats_score: dict                # {"score": int, "matched": list, "missing": list}
    matched_keywords: list
    missing_keywords: list
    
    # Application tracking
    application_id: Optional[str]
    application_status: str
    
    # Messages for debugging/logging
    messages: Annotated[list, add_messages]


# Backward compatibility alias
ApplicationState = GraphState


