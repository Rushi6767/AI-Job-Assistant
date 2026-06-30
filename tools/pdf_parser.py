"""
Tool for parsing PDF and DOCX resume files
"""
import PyPDF2
from docx import Document
from typing import Optional


def parse_pdf(file_path: str) -> str:
    """Extract text from PDF file"""
    try:
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text.strip()
    except Exception as e:
        return f"Error parsing PDF: {str(e)}"


def parse_docx(file_path: str) -> str:
    """Extract text from DOCX file"""
    try:
        doc = Document(file_path)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text.strip()
    except Exception as e:
        return f"Error parsing DOCX: {str(e)}"


def parse_resume(file_path: str) -> str:
    """Parse resume file (PDF, DOCX, or TXT)"""
    if file_path.lower().endswith('.pdf'):
        return parse_pdf(file_path)
    elif file_path.lower().endswith('.docx'):
        return parse_docx(file_path)
    elif file_path.lower().endswith('.txt'):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read().strip()
        except Exception as e:
            return f"Error parsing TXT: {str(e)}"
    else:
        return "Unsupported file format. Please upload PDF, DOCX, or TXT."


def parse_text_resume(text: str) -> str:
    """Handle plain text resume"""
    return text.strip()

