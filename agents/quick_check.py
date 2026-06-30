"""
Quick Check Agent - Runs suitability check on job description before full processing
"""
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from state import GraphState
from config import OPENAI_API_KEY, OPENAI_MODEL, TEMPERATURE
from agents.job_parser import parse_job_description


def quick_check_agent(state: GraphState) -> GraphState:
    """
    Perform a quick check on the job description suitability
    """
    # Sync backward compatibility fields
    jd_text = state.get("jd_text") or state.get("job_description", "")
    if not state.get("jd_text"):
        state["jd_text"] = jd_text
    if not state.get("job_description"):
        state["job_description"] = jd_text

    if not jd_text:
        state["quick_check_result"] = "Error: No job description provided."
        state["recommendation"] = "SKIP"
        state["messages"].append({"role": "system", "content": "No job description provided for Quick Check"})
        return state

    # Create LLM
    llm = ChatOpenAI(
        api_key=OPENAI_API_KEY,
        model=OPENAI_MODEL,
        temperature=0.0  # High determinism for rules
    )

    # Prompt template for Quick Check
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a job suitability scanner. Evaluate the provided Job Description (JD) and extract details about suitability, visa sponsorship, security clearance, and citizenship.

Rules for evaluation:
- Suitable for background:
  - Yes/Maybe: If the JD mentions Python, JavaScript/TypeScript, Django, React, FastAPI, Svelte, Web development, Full-stack, Backend, or general Software Engineer/Developer roles.
  - No: Stacks focusing exclusively on other languages (like C++, Java, C#, PHP, Go, Ruby, Swift, iOS, Android, Embedded) without Python, JavaScript/TypeScript, or web developer requirements.
- Visa sponsorship mentioned:
  - Yes (explicitly states they offer/support visa sponsorship or H1B transfer).
  - No (explicitly states they do NOT offer/support visa sponsorship, e.g. "no visa sponsorship", "cannot sponsor").
  - Not mentioned (sponsorship is not referenced in the JD text).
- Security clearance required: Yes (explicitly mentions secret clearance, top secret, TS/SCI, DoD clearance, security clearance required), No.
- Citizenship required: Yes (explicitly mentions US citizen required, must be a US citizen, citizenship required), No.

Determine the Recommendation according to these strict logical rules:
1. SKIP if: Security clearance is required (Yes) OR Citizenship is required (Yes) OR Visa sponsorship is explicitly "No" (e.g., "no sponsorship" explicitly stated).
2. APPLY if: (Suitable is "Yes" or "Maybe") AND there are no hard blockers (Clearance is No, Citizenship is No, and Visa sponsorship is either Yes or Not mentioned).
3. If Suitable is "No", recommend SKIP.

Format your output EXACTLY as follows (5 lines, no markdown bolding or styling):
Suitable for background: [Yes / No / Maybe]
Visa sponsorship mentioned: [Yes / No / Not mentioned]
Security clearance required: [Yes / No]
Citizenship required: [Yes / No]
Recommendation: [APPLY / SKIP / MAYBE]
"""),
        ("user", "Job Description:\n{job_description}")
    ])

    # Generate response
    chain = prompt | llm
    response = chain.invoke({"job_description": jd_text})
    content = response.content.strip()

    # Parse and clean output to ensure exact formatting
    lines = content.split('\n')
    clean_lines = []
    recommendation = "MAYBE"

    prefixes = [
        "Suitable for background:",
        "Visa sponsorship mentioned:",
        "Security clearance required:",
        "Citizenship required:",
        "Recommendation:"
    ]

    for line in lines:
        line = line.strip()
        if not line:
            continue
        for p in prefixes:
            if line.lower().startswith(p.lower()):
                val = line.split(":", 1)[1].strip()
                # Remove any markdown styling like asterisks or backticks
                val = val.replace("**", "").replace("`", "").strip()
                clean_lines.append(f"{p:<29} {val}")
                
                if p == "Recommendation:":
                    val_upper = val.upper()
                    if "SKIP" in val_upper:
                        recommendation = "SKIP"
                    elif "APPLY" in val_upper:
                        recommendation = "APPLY"
                    elif "MAYBE" in val_upper:
                        recommendation = "MAYBE"
                break

    # If parsing failed to get all lines, reconstruct or fall back
    if len(clean_lines) < 5:
        # Fallback raw storage
        state["quick_check_result"] = content
        # Basic regex/substring fallback for recommendation
        content_upper = content.upper()
        if "RECOMMENDATION: SKIP" in content_upper or "RECOMMENDATION:SKIP" in content_upper:
            recommendation = "SKIP"
        elif "RECOMMENDATION: APPLY" in content_upper or "RECOMMENDATION:APPLY" in content_upper:
            recommendation = "APPLY"
        else:
            recommendation = "MAYBE"
    else:
        state["quick_check_result"] = "\n".join(clean_lines)

    state["recommendation"] = recommendation
    state["messages"].append({
        "role": "system",
        "content": f"Quick check completed. Recommendation: {recommendation}"
    })

    # Always parse the job details (job_title, company_name, requirements, skills)
    # so they are available downstream or in the UI tracker, regardless of SKIP/APPLY status.
    state = parse_job_description(state)

    if recommendation == "SKIP":
        from agents.tracker import save_application
        state = save_application(state)

    return state
