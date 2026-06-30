"""
ATS Scorer Agent - Evaluates resume against JD and calculates ATS match score and keywords.
"""
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from state import GraphState
from config import OPENAI_API_KEY, OPENAI_MODEL, TEMPERATURE
from agents.tracker import save_application


def ats_score_agent(state: GraphState) -> GraphState:
    """
    Compare the resume against the JD, extract matched/missing keywords, and compute ATS score.
    """
    jd_text = state.get("jd_text") or state.get("job_description", "")
    resume_text = state.get("latex_resume") or state.get("tailored_resume") or state.get("resume_text") or state.get("user_resume", "")

    if not jd_text or not resume_text:
        state["ats_score"] = {"score": 0, "matched": [], "missing": []}
        state["matched_keywords"] = []
        state["missing_keywords"] = []
        state["match_score"] = 0.0
        state["skills_gap"] = []
        state = save_application(state)
        return state

    # Create LLM
    llm = ChatOpenAI(
        api_key=OPENAI_API_KEY,
        model=OPENAI_MODEL,
        temperature=0.0
    )

    # Prompt for ATS score & keywords
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are an expert ATS (Applicant Tracking System) reviewer. Compare the candidate's resume against the Job Description.

Analyze the resume and the job description to:
1. Identify all matched keywords (technical skills, methodologies, frameworks, languages mentioned in BOTH the JD and the resume).
2. Identify missing keywords (important technical skills, methodologies, frameworks, languages required by the JD but NOT mentioned in the resume).
3. Compute a realistic ATS Match Score (0 to 100) based on how well the resume matches the JD requirements.

Format your output EXACTLY as follows (3 lines, no markdown bolding or styling):
SCORE: [score number only, 0-100]
MATCHED: [comma-separated list of matched keywords]
MISSING: [comma-separated list of missing keywords]
"""),
        ("user", """Resume Content:
{resume}

Job Description:
{job_description}
""")
    ])

    # Generate response
    chain = prompt | llm
    response = chain.invoke({
        "resume": resume_text[:4000],  # Truncate to save tokens/prevent overflow
        "job_description": jd_text[:4000]
    })

    content = response.content.strip()
    lines = content.split("\n")

    score = 0
    matched = []
    missing = []

    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line.upper().startswith("SCORE:"):
            score_str = line.split(":", 1)[1].strip()
            try:
                score = int(score_str)
            except ValueError:
                score = 50
        elif line.upper().startswith("MATCHED:"):
            matched_str = line.split(":", 1)[1].strip()
            matched = [m.strip() for m in matched_str.split(",") if m.strip()]
        elif line.upper().startswith("MISSING:"):
            missing_str = line.split(":", 1)[1].strip()
            missing = [m.strip() for m in missing_str.split(",") if m.strip()]

    # Update state fields
    state["ats_score"] = {"score": score, "matched": matched, "missing": missing}
    state["matched_keywords"] = matched
    state["missing_keywords"] = missing
    state["match_score"] = score / 100.0
    state["skills_gap"] = missing

    state["messages"].append({
        "role": "system",
        "content": f"ATS Scorer completed. Score: {score}/100"
    })

    # Save the application using tracker
    state = save_application(state)

    return state
