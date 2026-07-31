"""
Resume Tailoring Agent - Utilities Package

Utility functions for resume parsing and job analysis.
Based on Uchenna's proven ATS-beating methodology.
"""

from .resume_parser import parse_resume, save_resume_data
from .job_analyzer import analyze_job_posting, find_exact_phrases

__version__ = "1.0.0"
__author__ = "Resume Tailoring Agent"

__all__ = [
    "parse_resume",
    "save_resume_data", 
    "analyze_job_posting",
    "find_exact_phrases"
]