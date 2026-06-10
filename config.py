"""
Configuration file for Job Application Assistant Agent
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# OPENAI_MODEL = "gpt-4"  # or "gpt-4-turbo" or "gpt-3.5-turbo"
OPENAI_MODEL = "gpt-3.5-turbo"  # Cheaper (90% less cost)

# Paths
DATA_DIR = "data"
RESUMES_DIR = os.path.join(DATA_DIR, "resumes")
CHROMA_DIR = os.path.join(DATA_DIR, "chroma_db")
APPLICATIONS_FILE = os.path.join(DATA_DIR, "applications.json")

# Create directories if they don't exist
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(RESUMES_DIR, exist_ok=True)
os.makedirs(CHROMA_DIR, exist_ok=True)

# Agent Configuration
MAX_TOKENS = 2000
TEMPERATURE = 0.7

# ChromaDB Configuration
COLLECTION_NAME = "job_applications"

