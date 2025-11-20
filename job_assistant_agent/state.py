"""
State definition for the Job Application Assistant Agent
"""
from typing import TypedDict, List, Optional, Annotated
from langgraph.graph import add_messages


class ApplicationState(TypedDict):
    """State object that flows through the agent workflow"""
    
    # Input
    job_url: Optional[str]
    job_description: str
    user_resume: str
    user_name: Optional[str]
    user_email: Optional[str]
    
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
    
    # Application tracking
    application_id: Optional[str]
    application_status: str
    
    # Messages for debugging/logging
    messages: Annotated[list, add_messages]

