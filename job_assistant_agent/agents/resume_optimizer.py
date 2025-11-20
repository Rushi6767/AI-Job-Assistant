"""
Resume Optimizer Agent - Tailors resume to match job requirements
"""
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from state import ApplicationState
from config import OPENAI_API_KEY, OPENAI_MODEL, MAX_TOKENS
from tools.vector_store import vector_store


def optimize_resume(state: ApplicationState) -> ApplicationState:
    """
    Tailor the user's resume to match job requirements
    Uses RAG to learn from past successful applications
    """
    user_resume = state.get("user_resume", "")
    job_title = state.get("job_title", "")
    company_name = state.get("company_name", "")
    job_skills = state.get("job_skills", [])
    job_requirements = state.get("job_requirements", [])
    
    if not user_resume:
        state["tailored_resume"] = ""
        return state
    
    # Search for similar past applications (RAG)
    query = f"{job_title} at {company_name}"
    similar_apps = vector_store.search_similar_applications(query, n_results=2)
    
    context = ""
    if similar_apps:
        context = "Here are examples of successful past applications:\n\n"
        for app in similar_apps:
            context += f"- {app['metadata'].get('job_title', 'N/A')}\n"
    
    # Create LLM
    llm = ChatOpenAI(
        api_key=OPENAI_API_KEY,
        model=OPENAI_MODEL,
        temperature=0.7,
        max_tokens=MAX_TOKENS
    )
    
    # Prompt template
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are an expert resume writer. Tailor the candidate's resume to match the job requirements.
        
        Instructions:
        1. Emphasize relevant experience and skills
        2. Use keywords from the job description
        3. Quantify achievements where possible
        4. Keep the same format but optimize content
        5. DO NOT add fake information
        6. Maintain professional tone
        
        {context}
        """),
        ("user", """Original Resume:
{resume}

Job Title: {job_title}
Company: {company}
Required Skills: {skills}
Requirements: {requirements}

Please provide an optimized version of the resume tailored for this position.
""")
    ])
    
    # Generate response
    chain = prompt | llm
    response = chain.invoke({
        "context": context,
        "resume": user_resume,
        "job_title": job_title,
        "company": company_name,
        "skills": ", ".join(job_skills),
        "requirements": ", ".join(job_requirements)
    })
    
    # Update state
    state["tailored_resume"] = response.content
    state["messages"].append({
        "role": "system",
        "content": "Resume optimized for job application"
    })
    
    return state

