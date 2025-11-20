# 💼 Job Application Assistant Agent

An intelligent AI agent that helps job seekers tailor their resumes and generate personalized cover letters using LangGraph and GPT-4.

## 🎯 Features

- **Job Description Parser**: Automatically extracts key requirements and skills
- **Skills Gap Analyzer**: Compares your resume with job requirements
- **Resume Optimizer**: Tailors your resume using RAG (learns from past applications)
- **Cover Letter Generator**: Creates personalized cover letters
- **Application Tracker**: Manages your job application pipeline

## 🛠️ Tech Stack

- **Framework**: LangGraph (Agent Orchestration)
- **LLM**: OpenAI GPT-4
- **Vector DB**: ChromaDB
- **UI**: Streamlit
- **Language**: Python 3.11+

## 📦 Installation

### 1. Clone or Download the Project

```bash
cd job_assistant_agent
```

### 2. Create Virtual Environment

```bash
python -m venv venv
```

### 3. Activate Virtual Environment

**Windows:**
```bash
.\venv\Scripts\Activate.ps1
```

**Mac/Linux:**
```bash
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Set Up Environment Variables

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

## 🚀 Usage

### Run the Streamlit App

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

### Using the Application

1. **Upload Resume**: Use the sidebar to upload your resume (PDF/DOCX) or paste text
2. **Add Job Description**: Paste the job posting in the main area
3. **Generate**: Click "Generate Application Materials"
4. **Review**: Check the tailored resume, cover letter, and skills analysis
5. **Track**: Monitor all your applications in the tracker tab

### Command Line Testing

You can also test the workflow directly:

```bash
python workflow.py
```

## 🏗️ Project Structure

```
job_assistant_agent/
├── agents/                  # Agent modules
│   ├── job_parser.py       # Parses job descriptions
│   ├── skills_analyzer.py  # Analyzes skills gap
│   ├── resume_optimizer.py # Tailors resumes
│   ├── cover_letter.py     # Generates cover letters
│   └── tracker.py          # Manages applications
├── tools/                   # Utility tools
│   ├── pdf_parser.py       # PDF/DOCX parsing
│   ├── web_scraper.py      # Job URL scraping
│   └── vector_store.py     # ChromaDB interface
├── data/                    # Data storage
│   ├── resumes/            # Uploaded resumes
│   ├── applications.json   # Application tracking
│   └── chroma_db/          # Vector embeddings
├── config.py               # Configuration
├── state.py                # State definition
├── workflow.py             # LangGraph workflow
├── app.py                  # Streamlit UI
└── requirements.txt        # Dependencies
```

## 🤖 How It Works

### Agent Workflow

```
User Input (Job + Resume)
    ↓
Job Parser Agent → Extract requirements, skills, company info
    ↓
Skills Analyzer → Compare resume with job requirements
    ↓
Resume Optimizer → Tailor resume (uses RAG for context)
    ↓
Cover Letter Generator → Create personalized letter
    ↓
Tracker Agent → Save application details
    ↓
Output (Tailored Resume + Cover Letter + Analysis)
```

### Design Pattern

This agent uses the **Multi-Agent Sequential Pipeline** pattern:
- **Modularity**: Each agent has a specific responsibility
- **State Management**: Shared state flows through all agents
- **RAG Integration**: Learns from past successful applications
- **Persistence**: Tracks applications for future reference

## 📊 Architecture

```
┌─────────────────────────────────────────┐
│         Streamlit UI (Frontend)         │
└───────────────┬─────────────────────────┘
                │
┌───────────────▼─────────────────────────┐
│    LangGraph Workflow Orchestrator      │
└───────────────┬─────────────────────────┘
                │
    ┌───────────┼───────────┬──────────┐
    │           │           │          │
┌───▼───┐  ┌───▼────┐  ┌───▼───┐  ┌──▼────┐
│ Job   │  │Skills  │  │Resume │  │Cover  │
│Parser │  │Analyzer│  │Optim. │  │Letter │
└───┬───┘  └───┬────┘  └───┬───┘  └──┬────┘
    │          │           │          │
    └──────────┴───────────┴──────────┘
                    │
            ┌───────▼────────┐
            │  Tracker Agent │
            └───────┬────────┘
                    │
        ┌───────────┴──────────┐
        │                      │
    ┌───▼────┐          ┌─────▼──────┐
    │ChromaDB│          │applications│
    │(Vector)│          │   .json    │
    └────────┘          └────────────┘
```

## 🎓 Assignment Context

This project was built for **CISC691 - Agentic AI**, Assignment 03: Building the AI Agent of Your Choice.

### Requirements Met

✅ **Problem Framing**: Solves real job application challenges  
✅ **Design Pattern**: Multi-agent sequential orchestration  
✅ **Architecture**: Modular, layered agent system  
✅ **Framework**: LangGraph for agent coordination  
✅ **AI Integration**: GPT-4 with RAG (ChromaDB)  
✅ **User Experience**: Streamlit UI with tracking  
✅ **Adaptability**: Learns from past applications  

## 🔧 Configuration

Edit `config.py` to customize:

```python
OPENAI_MODEL = "gpt-4"  # or "gpt-4-turbo" or "gpt-3.5-turbo"
MAX_TOKENS = 2000
TEMPERATURE = 0.7
```

## 📝 Future Improvements

- [ ] Add support for LinkedIn job scraping
- [ ] Multi-language support
- [ ] Interview preparation module
- [ ] Email integration for application submission
- [ ] Analytics dashboard
- [ ] A/B testing for resume versions

## ⚠️ Important Notes

- **API Costs**: This app uses OpenAI's GPT-4, which costs per token
- **Privacy**: Resume data is stored locally (never sent to external servers except OpenAI)
- **Customization**: Always review and personalize generated content
- **Accuracy**: AI-generated content may need human review

## 🤝 Contributing

This is an academic project. For improvements or issues, please contact the developer.

## 📄 License

Educational use only - CISC691 Fall 2025

## 👨‍💻 Author

**Your Name**  
University of Delaware - CISC691 Agentic AI  
Fall 2025

---

**Built with ❤️ using LangGraph, OpenAI, and Streamlit**

