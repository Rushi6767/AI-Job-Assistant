"""
Application Tracker Agent - Manages application records
"""
import json
import os
from datetime import datetime
from typing import Dict
from state import ApplicationState
from config import APPLICATIONS_FILE
from tools.vector_store import vector_store


def save_application(state: ApplicationState) -> ApplicationState:
    """
    Save application details to tracking system
    """
    # Load existing applications
    if os.path.exists(APPLICATIONS_FILE):
        with open(APPLICATIONS_FILE, 'r') as f:
            applications = json.load(f)
    else:
        applications = []
    
    # Create application record
    app_id = f"app_{len(applications) + 1}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    has_latex = bool(state.get("latex_resume"))
    has_tailored = bool(state.get("tailored_resume")) or has_latex
    
    application = {
        "id": app_id,
        "job_title": state.get("job_title", ""),
        "company": state.get("company_name", ""),
        "job_url": state.get("job_url", ""),
        "status": state.get("application_status", "drafted"),
        "match_score": state.get("match_score") if state.get("match_score") is not None else 0.0,
        "skills_gap": state.get("skills_gap", []),
        "date_created": datetime.now().isoformat(),
        "has_tailored_resume": has_tailored,
        "has_cover_letter": bool(state.get("cover_letter"))
    }
    
    applications.append(application)
    
    # Save to file
    with open(APPLICATIONS_FILE, 'w') as f:
        json.dump(applications, f, indent=2)
    
    # Add to vector store for future RAG
    resume_content = state.get("latex_resume") or state.get("tailored_resume", "")
    if resume_content and state.get("cover_letter"):
        vector_store.add_application(
            app_id=app_id,
            job_title=state.get("job_title", ""),
            company=state.get("company_name", ""),
            resume=resume_content,
            cover_letter=state.get("cover_letter", ""),
            metadata={
                "status": state.get("application_status", "drafted"),
                "match_score": state.get("match_score") if state.get("match_score") is not None else 0.0
            }
        )
    
    # Update state
    state["application_id"] = app_id
    state["messages"].append({
        "role": "system",
        "content": f"Application saved with ID: {app_id}"
    })
    
    # Append to tracker.md
    append_to_tracker_md(state)
    
    return state


def append_to_tracker_md(state: ApplicationState):
    """Append a row representing this run to tracker.md"""
    file_path = "tracker.md"
    date_str = datetime.now().strftime("%Y-%m-%d")
    company = state.get("company_name") or "N/A"
    role = state.get("job_title") or "N/A"
    recommendation = state.get("recommendation") or "N/A"
    
    ats_dict = state.get("ats_score")
    if ats_dict and "score" in ats_dict:
        ats_score = f"{ats_dict['score']}/100"
    elif state.get("match_score") is not None:
        ats_score = f"{int(state['match_score'] * 100)}/100"
    else:
        ats_score = "N/A"
        
    has_latex_str = "Yes" if state.get("latex_resume") else "No"
    
    row = f"| {date_str} | {company} | {role} | {recommendation} | {ats_score} | {has_latex_str} |\n"
    
    if not os.path.exists(file_path):
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("# Job Application Tracker\n\n")
            f.write("| Date | Company | Role | Recommendation | ATS Score | LaTeX Generated |\n")
            f.write("| --- | --- | --- | --- | --- | --- |\n")
            
    with open(file_path, "a", encoding="utf-8") as f:
        f.write(row)



def load_applications() -> list:
    """Load all tracked applications"""
    if os.path.exists(APPLICATIONS_FILE):
        with open(APPLICATIONS_FILE, 'r') as f:
            return json.load(f)
    return []


def update_application_status(app_id: str, new_status: str) -> bool:
    """Update the status of an application"""
    if not os.path.exists(APPLICATIONS_FILE):
        return False
    
    with open(APPLICATIONS_FILE, 'r') as f:
        applications = json.load(f)
    
    for app in applications:
        if app['id'] == app_id:
            app['status'] = new_status
            app['last_updated'] = datetime.now().isoformat()
            break
    
    with open(APPLICATIONS_FILE, 'w') as f:
        json.dump(applications, f, indent=2)
    
    return True

