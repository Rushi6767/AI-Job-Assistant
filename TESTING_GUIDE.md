# 🧪 Testing Guide for Job Application Assistant

## Quick Start Testing

### 1. Test API Connection

```bash
python test.py
```

Expected output: `API is working!`

---

## 2. Test Workflow (Command Line)

Create a test file `test_workflow.py`:

```python
from workflow import run_workflow

# Sample job description
job_description = """
Software Engineer at Google

Requirements:
- 5+ years of Python experience
- Experience with cloud platforms (AWS/GCP)
- Strong algorithms and data structures knowledge
- Bachelor's degree in Computer Science
- Experience with microservices architecture
- Knowledge of Docker and Kubernetes

Responsibilities:
- Design and implement scalable backend systems
- Collaborate with cross-functional teams
- Mentor junior engineers
"""

# Sample resume
resume = """
JOHN DOE
Software Engineer | john.doe@email.com

EXPERIENCE
Senior Python Developer | TechCorp (2019-Present)
- Built microservices handling 1M+ requests/day
- Migrated legacy systems to AWS
- Mentored team of 5 junior developers
- Implemented CI/CD pipelines with Docker

Python Developer | StartupXYZ (2017-2019)
- Developed REST APIs using Flask and FastAPI
- Optimized database queries (PostgreSQL)
- Reduced response time by 40%

EDUCATION
Bachelor of Science in Computer Science
University of Delaware, 2017

SKILLS
Python, FastAPI, AWS, Docker, PostgreSQL, Redis, Git
"""

# Run the workflow
print("🤖 Testing Job Application Assistant Agent...\n")
result = run_workflow(job_description, resume, "John Doe")

print("="*60)
print("RESULTS")
print("="*60)
print(f"\n📋 Job: {result['job_title']}")
print(f"🏢 Company: {result['company_name']}")
print(f"📊 Match Score: {result['match_score']*100:.1f}%")
print(f"\n⚠️ Skills Gap: {', '.join(result['skills_gap']) if result['skills_gap'] else 'None'}")
print(f"\n✅ Application ID: {result['application_id']}")
print(f"\n📝 Resume Length: {len(result['tailored_resume'])} characters")
print(f"✉️ Cover Letter Length: {len(result['cover_letter'])} characters")

print("\n" + "="*60)
print("✅ Workflow test completed successfully!")
print("="*60)
```

Run it:
```bash
python test_workflow.py
```

---

## 3. Test Streamlit UI

```bash
streamlit run app.py
```

### Manual Testing Checklist

#### Test Case 1: Upload Resume
- [ ] Upload a PDF resume
- [ ] Upload a DOCX resume
- [ ] Paste text resume
- [ ] Verify preview shows correctly

#### Test Case 2: Generate Application
- [ ] Paste job description
- [ ] Click "Generate Application Materials"
- [ ] Wait for processing (30-60 seconds)
- [ ] Verify all tabs show content:
  - Tailored Resume
  - Cover Letter
  - Skills Analysis

#### Test Case 3: Application Tracker
- [ ] Navigate to "Application Tracker" tab
- [ ] Verify application appears in list
- [ ] Update application status
- [ ] Verify status change persists

#### Test Case 4: Download Features
- [ ] Download tailored resume
- [ ] Download cover letter
- [ ] Verify files are readable

---

## 4. Test Individual Components

### Test PDF Parser

```python
from tools.pdf_parser import parse_resume

# Test with your PDF
text = parse_resume("path/to/resume.pdf")
print(text)
```

### Test Job Parser

```python
from agents.job_parser import parse_job_description
from state import ApplicationState

state = {
    "job_description": "Your job description here...",
    "messages": []
}

result = parse_job_description(state)
print(f"Job Title: {result['job_title']}")
print(f"Company: {result['company_name']}")
print(f"Skills: {result['job_skills']}")
```

### Test Vector Store

```python
from tools.vector_store import vector_store

# Add test application
vector_store.add_application(
    app_id="test_001",
    job_title="Software Engineer",
    company="Google",
    resume="Sample resume...",
    cover_letter="Sample letter...",
    metadata={"status": "applied"}
)

# Search similar
results = vector_store.search_similar_applications("Software Engineer")
print(results)
```

---

## 5. Sample Test Data

### Sample Job Description 1: Entry-Level Software Engineer

```
Entry-Level Software Engineer at StartupXYZ

Requirements:
- Bachelor's degree in Computer Science
- 0-2 years of programming experience
- Knowledge of Python or JavaScript
- Understanding of data structures and algorithms
- Git version control experience
- Strong problem-solving skills

Responsibilities:
- Write clean, maintainable code
- Participate in code reviews
- Learn from senior team members
- Contribute to team projects
```

### Sample Job Description 2: Senior Data Scientist

```
Senior Data Scientist at DataCorp

Requirements:
- 7+ years in data science/machine learning
- PhD or Master's in related field
- Expert in Python, R, SQL
- Experience with TensorFlow, PyTorch, scikit-learn
- Strong statistical analysis skills
- Experience with big data tools (Spark, Hadoop)
- Published research papers preferred

Responsibilities:
- Build ML models for production
- Lead data science initiatives
- Mentor junior data scientists
- Present findings to stakeholders
```

### Sample Job Description 3: Frontend Developer

```
Frontend Developer at WebAgency

Requirements:
- 3+ years of frontend development
- Expert in React.js and TypeScript
- Experience with CSS frameworks (Tailwind, Material-UI)
- Knowledge of state management (Redux, Zustand)
- Understanding of responsive design
- Experience with REST APIs
- Portfolio of web projects

Responsibilities:
- Build responsive web applications
- Optimize for performance
- Collaborate with designers
- Write clean, reusable components
```

---

## 6. Expected Behavior

### Successful Test Output

✅ **Job Parser**: Correctly extracts title, company, skills  
✅ **Skills Analyzer**: Identifies gaps, calculates match score  
✅ **Resume Optimizer**: Tailors content with relevant keywords  
✅ **Cover Letter**: Generates personalized 3-4 paragraphs  
✅ **Tracker**: Saves application with unique ID  

### Performance Benchmarks

- **Total workflow time**: 30-60 seconds
- **API calls**: ~4-5 per workflow run
- **Resume optimization**: 10-20 seconds
- **Cover letter generation**: 10-15 seconds

---

## 7. Troubleshooting

### Common Issues

**Issue**: `ImportError: No module named 'langgraph'`
**Solution**: Install dependencies: `pip install -r requirements.txt`

**Issue**: `openai.AuthenticationError`
**Solution**: Check `.env` file has correct API key

**Issue**: `ChromaDB connection error`
**Solution**: Delete `data/chroma_db/` and restart

**Issue**: Streamlit stuck on "Running..."
**Solution**: Check OpenAI API rate limits, try again in a minute

**Issue**: Empty resume/cover letter output
**Solution**: Increase MAX_TOKENS in `config.py`

---

## 8. Validation Checklist

Before submitting/presenting:

- [ ] API key is working
- [ ] All dependencies installed
- [ ] Can upload PDF/DOCX resumes
- [ ] Job descriptions parse correctly
- [ ] Generated resumes are relevant
- [ ] Cover letters are personalized
- [ ] Skills analysis makes sense
- [ ] Applications save to tracker
- [ ] Can update application status
- [ ] Download buttons work
- [ ] No crashes or errors
- [ ] Performance is acceptable (< 2 min)

---

## 9. Video Recording Test Script

Use this script for your walkthrough video:

1. **Introduction** (30 sec)
   - "This is the Job Application Assistant Agent"
   - Show the UI homepage

2. **Upload Resume** (30 sec)
   - Upload sample PDF/DOCX
   - Show preview

3. **Paste Job Description** (30 sec)
   - Use one of the sample jobs above
   - Click generate

4. **Show Results** (2-3 min)
   - Show match score
   - Display tailored resume
   - Display cover letter
   - Explain skills analysis

5. **Application Tracker** (1 min)
   - Show saved application
   - Update status
   - Explain tracking features

6. **Technical Highlights** (2 min)
   - Explain LangGraph workflow
   - Show architecture diagram
   - Mention RAG and vector storage

7. **Conclusion** (30 sec)
   - Recap benefits
   - Mention future improvements

---

## 10. Automated Testing (Future)

Create `test_agents.py` for unit tests:

```python
import unittest
from agents.job_parser import parse_job_description

class TestJobParser(unittest.TestCase):
    def test_parse_basic_job(self):
        state = {
            "job_description": "Software Engineer at Google. Python required.",
            "messages": []
        }
        result = parse_job_description(state)
        self.assertIsNotNone(result['job_title'])
        self.assertIsNotNone(result['company_name'])

if __name__ == '__main__':
    unittest.main()
```

---

✅ **Testing Complete!** Your agent is ready for demonstration.

