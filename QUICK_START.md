# 🚀 Quick Start Guide

## Step 1: Verify Installation ✅

Your environment should already be set up. To verify:

```bash
# Make sure you're in the project directory
cd C:\Users\satha\OneDrive\Desktop\a03_agentic_ai\job_assistant_agent

# Activate virtual environment (if not already active)
.\venv\Scripts\Activate.ps1

# Verify key packages
python -c "import langgraph, streamlit, chromadb; print('✅ All packages installed!')"
```

---

## Step 2: Test Your API Key 🔑

```bash
python test.py
```

Expected output: `API is working!`

---

## Step 3: Test the Workflow (Optional) 🧪

This tests the complete agent workflow without the UI:

```bash
python test_workflow.py
```

**What this does:**
- Runs all 5 agents in sequence
- Uses sample job description and resume
- Shows tailored resume and cover letter
- Takes ~30-60 seconds

**Expected output:**
- Job title and company extracted
- Match score (0-100%)
- Skills gap analysis
- Generated resume preview
- Generated cover letter preview
- Application saved to `data/applications.json`

---

## Step 4: Run the Streamlit App 🎨

```bash
streamlit run app.py
```

**What happens:**
1. Browser opens at `http://localhost:8501`
2. You'll see the Job Application Assistant interface

---

## Step 5: Use the Application 💼

### Create Your First Application

1. **Upload Resume** (Sidebar):
   - Enter your name
   - Upload PDF/DOCX or paste text
   - Check the preview

2. **Add Job Description** (Main Area):
   - Optional: Paste job URL
   - Required: Paste full job description
   - Click "Generate Application Materials"

3. **Wait** (~30-60 seconds):
   - Agent workflow runs
   - Processing indicator shows progress

4. **Review Results**:
   - Check match score
   - Review tailored resume
   - Read cover letter
   - See skills gap analysis

5. **Download**:
   - Download tailored resume
   - Download cover letter

6. **Track**:
   - Go to "Application Tracker" tab
   - See all saved applications
   - Update status as you progress

---

## Step 6: Prepare for Video Demo 🎥

### Recording Checklist

- [ ] Close unnecessary browser tabs
- [ ] Clear notifications
- [ ] Have sample resume ready
- [ ] Have 2-3 job descriptions ready
- [ ] Prepare talking points

### Demo Script (6-10 minutes)

**1. Introduction (30 sec)**
- "This is my Job Application Assistant Agent"
- "Built with LangGraph and OpenAI GPT-4"
- Show the homepage

**2. System Overview (1 min)**
- Explain the problem it solves
- Mention 5 agents working together
- Show the workflow diagram (from TECHNICAL_REPORT.md)

**3. Live Demo (3-4 min)**
- Upload resume
- Paste job description
- Click generate
- Show loading (speed up video if needed)
- Display results:
  - Match score
  - Tailored resume
  - Cover letter
  - Skills analysis

**4. Application Tracker (1 min)**
- Show saved applications
- Update status
- Explain tracking features

**5. Technical Deep Dive (2-3 min)**
- Show architecture diagram
- Explain LangGraph workflow
- Mention RAG with ChromaDB
- Discuss design decisions

**6. Conclusion (30 sec)**
- Recap benefits
- Mention future improvements
- Thank viewers

---

## Troubleshooting 🔧

### Common Issues

**Issue**: `ImportError: No module named 'langgraph'`  
**Fix**: `pip install -r requirements.txt`

**Issue**: `openai.AuthenticationError`  
**Fix**: Check `.env` file has correct `OPENAI_API_KEY`

**Issue**: Streamlit won't start  
**Fix**: Make sure virtual environment is activated

**Issue**: Resume not parsing correctly  
**Fix**: Try pasting text directly instead of uploading

**Issue**: Empty output  
**Fix**: Check OpenAI API has credits, increase MAX_TOKENS in config.py

---

## Project Files Overview 📁

```
job_assistant_agent/
├── 📄 app.py                    # Main Streamlit UI
├── 📄 workflow.py               # LangGraph orchestration
├── 📄 state.py                  # State definition
├── 📄 config.py                 # Configuration
├── 📄 requirements.txt          # Dependencies
├── 📄 test_workflow.py          # Test script
├── 📄 README.md                 # Project overview
├── 📄 TECHNICAL_REPORT.md       # Detailed documentation
├── 📄 TESTING_GUIDE.md          # Testing instructions
├── 📄 QUICK_START.md            # This file
│
├── 📁 agents/                   # Agent implementations
│   ├── job_parser.py
│   ├── skills_analyzer.py
│   ├── resume_optimizer.py
│   ├── cover_letter.py
│   └── tracker.py
│
├── 📁 tools/                    # Utility tools
│   ├── pdf_parser.py
│   ├── web_scraper.py
│   └── vector_store.py
│
└── 📁 data/                     # Generated during use
    ├── resumes/                 # Uploaded files
    ├── applications.json        # Tracking database
    └── chroma_db/               # Vector embeddings
```

---

## Testing with Different Job Types 🎯

### Test Case 1: Software Engineer
Use `test_workflow.py` as-is

### Test Case 2: Data Scientist
Replace job description with:
```
Data Scientist at Meta
- PhD in CS/Stats/ML
- 5+ years experience
- Python, R, SQL, TensorFlow
- Strong statistics background
```

### Test Case 3: Product Manager
```
Product Manager at Apple
- 7+ years product management
- Technical background
- Excellent communication
- User-centered design thinking
```

---

## Next Steps After Building 📝

### 1. Complete Technical Report
- Use `TECHNICAL_REPORT.md` as template
- Add your name and details
- Include screenshots
- Export as PDF (max 10 pages)

### 2. Record Video Walkthrough
- Use OBS Studio, Loom, or Zoom
- Follow demo script above
- 6-10 minutes
- Upload to YouTube (unlisted)

### 3. Export Workflow
Save this file as `workflow_export.txt`:
```
Job Application Assistant Agent - Workflow Export

Graph Structure:
- Entry Point: parse_job
- Node 1: parse_job (Job Parser Agent)
- Node 2: analyze_skills (Skills Analyzer Agent)
- Node 3: optimize_resume (Resume Optimizer Agent)
- Node 4: generate_cover_letter (Cover Letter Generator Agent)
- Node 5: save_application (Tracker Agent)

Edges:
parse_job → analyze_skills
analyze_skills → optimize_resume
optimize_resume → generate_cover_letter
generate_cover_letter → save_application
save_application → END

State Schema: See state.py
```

### 4. Prepare Submission
Create a text file with:
```
Job Application Assistant Agent

GitHub/Drive Link: [your link]
YouTube Video: [your link]
Technical Report: [attached PDF]
Workflow Export: [attached file]

Short Description:
An intelligent multi-agent system that helps job seekers tailor resumes
and generate cover letters. Built with LangGraph, uses 5 specialized agents,
includes RAG with ChromaDB, and features a Streamlit UI for easy interaction.
```

---

## Tips for Success 💡

1. **Test Thoroughly**: Run with different job types
2. **Customize Prompts**: Edit agent files to improve output
3. **Add Your Touch**: Personalize the UI or add features
4. **Document Changes**: Keep notes for your report
5. **Practice Demo**: Rehearse your video walkthrough
6. **Save Examples**: Screenshot good results for presentation

---

## Support Resources 📚

- **LangGraph Docs**: https://langchain-ai.github.io/langgraph/
- **Streamlit Docs**: https://docs.streamlit.io/
- **OpenAI API**: https://platform.openai.com/docs
- **Project README**: See README.md
- **Technical Report**: See TECHNICAL_REPORT.md
- **Testing Guide**: See TESTING_GUIDE.md

---

## Questions? 🤔

Check these files:
- **General overview**: README.md
- **Technical details**: TECHNICAL_REPORT.md
- **Testing help**: TESTING_GUIDE.md
- **Code structure**: Look at agent files

---

✅ **You're all set! Start with Step 4 (Run Streamlit App) and create your first application!**

