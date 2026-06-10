"""
Skills Gap Analyzer Agent - Compares user skills with job requirements
"""
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from state import ApplicationState
from config import OPENAI_API_KEY, OPENAI_MODEL, TEMPERATURE


def analyze_skills_gap(state: ApplicationState) -> ApplicationState:
    """
    Analyze the gap between user's skills and job requirements
    """
    user_resume = state.get("user_resume", "")
    job_skills = state.get("job_skills", [])
    job_requirements = state.get("job_requirements", [])
    
    if not user_resume or not job_skills:
        state["skills_gap"] = []
        state["match_score"] = 0.0
        return state
    
    # Create LLM
    llm = ChatOpenAI(
        api_key=OPENAI_API_KEY,
        model=OPENAI_MODEL,
        temperature=TEMPERATURE
    )
    
    # Prompt template
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a skills gap analyzer. Compare the candidate's resume with job requirements.
        
        Analyze:
        1. Which required skills are missing from the resume
        2. Overall match score (0-100%)
        3. Recommendations for improvement
        
        Format your response as:
        MISSING_SKILLS: [skill1, skill2, ...]
        MATCH_SCORE: [number]
        RECOMMENDATIONS: [brief suggestions]
        """),
        ("user", """Resume:
{resume}

Required Skills:
{skills}

Requirements:
{requirements}
""")
    ])
    
    # Generate response
    chain = prompt | llm
    response = chain.invoke({
        "resume": user_resume,
        "skills": ", ".join(job_skills),
        "requirements": ", ".join(job_requirements)
    })
    
    # Parse response
    content = response.content
    lines = content.split('\n')
    
    missing_skills = []
    match_score = 0.0
    
    for line in lines:
        if line.startswith("MISSING_SKILLS:"):
            skills_str = line.replace("MISSING_SKILLS:", "").strip()
            missing_skills = [s.strip() for s in skills_str.split(',') if s.strip()]
        elif line.startswith("MATCH_SCORE:"):
            score_str = line.replace("MATCH_SCORE:", "").strip().replace('%', '')
            try:
                match_score = float(score_str) / 100.0
            except:
                match_score = 0.5
    
    # Update state
    state["skills_gap"] = missing_skills
    state["match_score"] = match_score
    state["messages"].append({
        "role": "system",
        "content": f"Skills analysis complete. Match score: {match_score*100:.0f}%"
    })
    
    return state

