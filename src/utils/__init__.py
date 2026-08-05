"""
Resume Tailoring Agent - Utilities Package

Utility functions for resume parsing, job analysis, validation, and output generation.
Based on Uchenna's proven ATS-beating methodology.
"""

from .resume_parser import parse_pdf_resume
from .job_analyzer import extract_keywords
from .resume_generator import generate_docx_resume
from .validation import ResumeValidator
from .context import ContextGatherer

__all__ = [
    'parse_pdf_resume',
    'extract_keywords',
    'generate_docx_resume',
    'ResumeValidator',
    'ContextGatherer'
]

__version__ = "1.0.0"
__author__ = "Resume Tailoring Agent"

__all__ = [
    "parse_resume",
    "save_resume_data", 
    "analyze_job_posting",
    "find_exact_phrases"
]