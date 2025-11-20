"""
Job Parser Agent - Extracts structured information from job descriptions
"""
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from state import ApplicationState
from config import OPENAI_API_KEY, OPENAI_MODEL, TEMPERATURE


def parse_job_description(state: ApplicationState) -> ApplicationState:
    """
    Parse job description and extract key information
    """
    job_description = state.get("job_description", "")
    
    if not job_description:
        state["messages"].append({"role": "system", "content": "No job description provided"})
        return state
    
    # Create LLM
    llm = ChatOpenAI(
        api_key=OPENAI_API_KEY,
        model=OPENAI_MODEL,
        temperature=TEMPERATURE
    )
    
    # Prompt template
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a job description analyzer. Extract structured information from the job posting.
        
        Extract:
        1. Job Title
        2. Company Name
        3. Required Skills (list)
        4. Key Requirements (list)
        5. Responsibilities
        
        Format your response as:
        JOB_TITLE: [title]
        COMPANY: [company name]
        SKILLS: [skill1, skill2, skill3, ...]
        REQUIREMENTS: [req1, req2, req3, ...]
        """),
        ("user", "Job Description:\n{job_description}")
    ])
    
    # Generate response
    chain = prompt | llm
    response = chain.invoke({"job_description": job_description})
    
    # Parse the response
    content = response.content
    lines = content.split('\n')
    
    job_title = ""
    company_name = ""
    skills = []
    requirements = []
    
    for line in lines:
        if line.startswith("JOB_TITLE:"):
            job_title = line.replace("JOB_TITLE:", "").strip()
        elif line.startswith("COMPANY:"):
            company_name = line.replace("COMPANY:", "").strip()
        elif line.startswith("SKILLS:"):
            skills_str = line.replace("SKILLS:", "").strip()
            skills = [s.strip() for s in skills_str.split(',') if s.strip()]
        elif line.startswith("REQUIREMENTS:"):
            req_str = line.replace("REQUIREMENTS:", "").strip()
            requirements = [r.strip() for r in req_str.split(',') if r.strip()]
    
    # Update state
    state["job_title"] = job_title
    state["company_name"] = company_name
    state["job_skills"] = skills
    state["job_requirements"] = requirements
    state["messages"].append({
        "role": "system",
        "content": f"Parsed job: {job_title} at {company_name}"
    })
    
    return state

