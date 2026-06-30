"""
Resume LaTeX Agent - Generates a raw LaTeX resume tailored to the JD using Rushi's details.
"""
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from state import GraphState
from config import OPENAI_API_KEY, OPENAI_MODEL, MAX_TOKENS
from tools.vector_store import vector_store


def resume_latex_agent(state: GraphState) -> GraphState:
    """
    Tailor candidate's resume and output compile-ready LaTeX content
    """
    jd_text = state.get("jd_text") or state.get("job_description", "")
    job_title = state.get("job_title", "Software Engineer")
    company_name = state.get("company_name", "Company")
    job_skills = state.get("job_skills", [])
    job_requirements = state.get("job_requirements", [])

    # Search for similar past applications from RAG if any
    query = f"{job_title} at {company_name}"
    similar_apps = vector_store.search_similar_applications(query, n_results=2)
    
    rag_context = ""
    if similar_apps:
        rag_context = "Here are examples of successful past applications to draw context from:\n\n"
        for app in similar_apps:
            rag_context += f"- {app['metadata'].get('job_title', 'N/A')}\n"

    # Create LLM
    llm = ChatOpenAI(
        api_key=OPENAI_API_KEY,
        model=OPENAI_MODEL,
        temperature=0.4,
        max_tokens=MAX_TOKENS
    )

    # Prompt Template for LaTeX Generation
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are an expert resume writer. Generate a tailored, ATS-optimized LaTeX resume for Rushi Sathavara based on the job description.
The output MUST be a complete, valid, compilable LaTeX document.
CRITICAL: Output ONLY the raw LaTeX code. Do NOT wrap the code in markdown code blocks (e.g. ```latex or ```), and do NOT include any introductory or concluding text.

LaTeX Structure & Constraint Rules:
- No `\\includegraphics`, no `tabular`, no `\\begin{{multicols}}` — ATS parsers choke on these.
- No color packages (hyperref links OK but use `urlcolor=black`).
- Bullet points via `itemize` only.
- Every bullet point must start with a strong action verb (Led, Built, Designed, Reduced, Improved...).
- Metrics must be preserved exactly (e.g. "80% reduction in failures", "50% reduction in prep time", "35% increase in velocity").
- JD keywords must appear naturally in bullets — not stuffed into skills section alone.
- Phone number must be exactly: (929) 548-2415
- GPA must be exactly: 4.0/4.0
- LinkedIn URL must always be: https://linkedin.com/in/rushi-sathavara-abb68418b

Structure to populate:
\\documentclass[letterpaper,11pt]{{article}}
\\usepackage[left=0.5in,right=0.5in,top=0.5in,bottom=0.5in]{{geometry}}
\\usepackage{{enumitem}}
\\usepackage{{titlesec}}
\\usepackage{{hyperref}}
\\usepackage{{fontenc}}
\\usepackage{{inputenc}}

\\hypersetup{{colorlinks=true, urlcolor=black}}
\\setlength{{\\parindent}}{{0pt}}
\\pagestyle{{empty}}

% Section formatting
\\titleformat{{\\section}}{{\\large\\bfseries}}{{}}{{0em}}{{}}[\\titlerule]
\\titlespacing{{\\section}}{{0pt}}{{6pt}}{{4pt}}

\\begin{{document}}

%--- HEADER ---%
\\begin{{center}}
    {{\\LARGE \\textbf{{Rushi Sathavara}}}} \\\\[4pt]
    (929) 548-2415 \\quad | \\quad
    \\href{{mailto:sathawararushi@gmail.com}}{{sathawararushi@gmail.com}} \\quad | \\quad
    \\href{{https://linkedin.com/in/rushi-sathavara-abb68418b}}{{LinkedIn}} \\quad | \\quad
    \\href{{https://github.com/Rushi6767}}{{GitHub}} \\quad | \\quad
    \\href{{https://my-portfolio-beige-xi-93.vercel.app/}}{{Portfolio}}
\\end{{center}}

\\section{{Summary}}
% Generate 2-3 sentences summary tailored to the JD. Lead with role title from JD (e.g. "Experienced Full-Stack Engineer targeting [role]...").

\\section{{Technical Skills}}
% Comma-separated skills tailored to the JD. NO tables, NO columns.
\\textbf{{Languages:}} ...\\\\
\\textbf{{Frameworks:}} ...\\\\
\\textbf{{Databases:}} ...\\\\
\\textbf{{Cloud \\& DevOps:}} ...\\\\
\\textbf{{AI/ML:}} ...

\\section{{Experience}}

\\textbf{{Full-Stack Developer}} \\hfill \\textit{{Mar 2024 -- Dec 2025}}\\\\
\\textit{{Harrisburg University — Center for Innovation \\& Entrepreneurship, Harrisburg, PA}}
\\begin{{itemize}}[leftmargin=*, noitemsep, topsep=2pt]
    % Bullet points here. Tailor using Rushi's details:
    % - Built Print3D platform with Svelte frontend and Python backend, enabling 3D model upload, preview, and print management.
    % - Developed multi-file cart system with persistent state and REST APIs for frontend consumption.
    % - Implemented CI/CD pipeline with Docker, ensuring zero-downtime deployment.
    % - Optimized database queries and backend performance for large 3D model datasets.
\\end{{itemize}}

\\textbf{{Full-Stack Developer}} \\hfill \\textit{{Sep 2021 -- Jul 2022}}\\\\
\\textit{{LinkSture Technologies Pvt. Ltd., Ahmedabad, India}}
\\begin{{itemize}}[leftmargin=*, noitemsep, topsep=2pt]
    % Bullet points here. Tailor using Rushi's details:
    % - Designed Django REST APIs for Shopify integration and real-time inventory synchronization.
    % - Built React dashboards and admin interfaces with backend data analytics.
    % - Implemented Celery/Redis task queues for background jobs, reducing failures by 80%.
\\end{{itemize}}

\\textbf{{Team Lead \\& Python Developer}} \\hfill \\textit{{Dec 2019 -- Sep 2021}}\\\\
\\textit{{Odoo (Tiny ERP), Gandhinagar, India}}
\\begin{{itemize}}[leftmargin=*, noitemsep, topsep=2pt]
    % Bullet points here. Tailor using Rushi's details:
    % - Led full-stack development of OCR invoice processing system with backend APIs and frontend dashboards.
    % - Implemented CI/CD pipeline reducing deployment preparation time by 50%.
    % - Mentored team in Agile practices, increasing development velocity by 35%.
\\end{{itemize}}

\\section{{Projects}}
% Choose the 2 or 3 most relevant projects from Rushi's projects:
% 1. Shopify E-commerce Integration Platform (Django — React — DRF — Celery)
% 2. AI Chatbot with RAG (FastAPI — Streamlit — LangChain — LangGraph)
% 3. Print3D - 3D Printing Platform (Svelte — TypeScript — Python — Docker)
% 4. WhatsApp Analytics Dashboard (Flask — Python — Pandas — Matplotlib)
% Format each project as:
% \\textbf{{[Project Name]}} \\hfill \\textit{{[Stack keywords]}}
% \\begin{{itemize}}[leftmargin=*, noitemsep, topsep=2pt]
%     \\item ...
% \\end{{itemize}}

\\section{{Education}}
\\textbf{{M.S. in Computer Science}} \\hfill \\textit{{Jan 2024 -- Dec 2025}}\\\\
Harrisburg University of Science and Technology, Harrisburg, PA \\quad GPA: 4.0/4.0

\\textbf{{B.E. in Computer Engineering}} \\hfill \\textit{{Aug 2015 -- Apr 2019}}\\\\
Silver Oak College of Engineering \\& Technology, Ahmedabad, India

\\end{{document}}
"""),
        ("user", """Job Description:
{job_description}

Job Title: {job_title}
Company: {company_name}
Required Skills: {job_skills}
Requirements: {job_requirements}

{rag_context}
""")
    ])

    # Generate response
    chain = prompt | llm
    response = chain.invoke({
        "job_description": jd_text,
        "job_title": job_title,
        "company_name": company_name,
        "job_skills": ", ".join(job_skills),
        "job_requirements": ", ".join(job_requirements),
        "rag_context": rag_context
    })

    # Sanitize and strip markdown code blocks if LLM included them
    content = response.content.strip()
    if content.startswith("```"):
        lines = content.split("\n")
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines[-1].strip() == "```":
            lines = lines[:-1]
        content = "\n".join(lines).strip()

    # Update state
    state["latex_resume"] = content
    state["tailored_resume"] = content  # Keep aligned for compatibility
    state["messages"].append({
        "role": "system",
        "content": "Tailored LaTeX resume generated successfully."
    })

    return state
