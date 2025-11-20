"""
Cover Letter Generator Agent - Creates personalized cover letters
"""
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from state import ApplicationState
from config import OPENAI_API_KEY, OPENAI_MODEL, MAX_TOKENS


def generate_cover_letter(state: ApplicationState) -> ApplicationState:
    """
    Generate a personalized cover letter based on job and resume
    """
    user_resume = state.get("user_resume", "")
    user_name = state.get("user_name", "Your Name")
    job_title = state.get("job_title", "")
    company_name = state.get("company_name", "")
    job_requirements = state.get("job_requirements", [])
    
    if not user_resume or not job_title:
        state["cover_letter"] = ""
        return state
    
    # Create LLM
    llm = ChatOpenAI(
        api_key=OPENAI_API_KEY,
        model=OPENAI_MODEL,
        temperature=0.7,
        max_tokens=MAX_TOKENS
    )
    
    # Prompt template
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are an expert cover letter writer. Create a compelling, personalized cover letter.
        
        Structure:
        1. Opening: Express enthusiasm for the role
        2. Body: Highlight 2-3 relevant experiences/skills
        3. Closing: Express interest in discussing further
        
        Guidelines:
        - Keep it to 3-4 paragraphs
        - Be specific and authentic
        - Show genuine interest in the company
        - Match tone to company culture
        - Use confident but humble language
        """),
        ("user", """Resume Summary:
{resume}

Job Title: {job_title}
Company: {company}
Key Requirements: {requirements}

Candidate Name: {name}

Generate a professional cover letter for this application.
""")
    ])
    
    # Generate response
    chain = prompt | llm
    response = chain.invoke({
        "resume": user_resume[:1500],  # Limit resume length
        "job_title": job_title,
        "company": company_name,
        "requirements": ", ".join(job_requirements[:5]),  # Top 5 requirements
        "name": user_name
    })
    
    # Update state
    state["cover_letter"] = response.content
    state["messages"].append({
        "role": "system",
        "content": "Cover letter generated"
    })
    
    return state

