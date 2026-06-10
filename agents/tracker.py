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
    
    application = {
        "id": app_id,
        "job_title": state.get("job_title", ""),
        "company": state.get("company_name", ""),
        "job_url": state.get("job_url", ""),
        "status": state.get("application_status", "drafted"),
        "match_score": state.get("match_score", 0.0),
        "skills_gap": state.get("skills_gap", []),
        "date_created": datetime.now().isoformat(),
        "has_tailored_resume": bool(state.get("tailored_resume")),
        "has_cover_letter": bool(state.get("cover_letter"))
    }
    
    applications.append(application)
    
    # Save to file
    with open(APPLICATIONS_FILE, 'w') as f:
        json.dump(applications, f, indent=2)
    
    # Add to vector store for future RAG
    if state.get("tailored_resume") and state.get("cover_letter"):
        vector_store.add_application(
            app_id=app_id,
            job_title=state.get("job_title", ""),
            company=state.get("company_name", ""),
            resume=state.get("tailored_resume", ""),
            cover_letter=state.get("cover_letter", ""),
            metadata={
                "status": state.get("application_status", "drafted"),
                "match_score": state.get("match_score", 0.0)
            }
        )
    
    # Update state
    state["application_id"] = app_id
    state["messages"].append({
        "role": "system",
        "content": f"Application saved with ID: {app_id}"
    })
    
    return state


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

