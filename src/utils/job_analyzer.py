"""
Job Description Analyzer

Utility functions for extracting key information from job descriptions.
Implements Uchenna's keyword extraction methodology.
"""

import re
from collections import Counter

def extract_keywords(job_description):
    """
    Extract key terms from job description.
    
    Args:
        job_description (str): The job posting text
    
    Returns:
        dict: Extracted keywords and phrases
    """
    try:
        # Basic keyword extraction structure
        # In real implementation, use more sophisticated NLP
        
        keywords = {
            "technical_skills": [],
            "role_keywords": [],
            "company_values": [],
            "requirements": [],
            "responsibilities": []
        }
        
        text = job_description.lower()
        
        # Simple keyword patterns (expand these)
        tech_patterns = [
            r'sql', r'python', r'excel', r'tableau', r'power bi',
            r'data analysis', r'machine learning', r'statistics'
        ]
        
        for pattern in tech_patterns:
            if re.search(pattern, text):
                keywords["technical_skills"].append(pattern)
        
        return {
            "status": "success",
            "keywords": keywords,
            "message": "Use AI for better keyword extraction"
        }
        
    except Exception as e:
        return {"status": "error", "message": str(e)}

def find_exact_phrases(job_description):
    """
    Find exact phrases that should be copied verbatim.
    
    This implements Uchenna's core strategy of verbatim keyword matching.
    
    Args:
        job_description (str): Job posting text
    
    Returns:
        list: Exact phrases to copy
    """
    try:
        # Look for common phrase patterns
        phrases = []
        
        # Pattern for skills descriptions
        skill_patterns = [
            r'strong .+ skills?',
            r'experience with .+',
            r'proficient in .+',
            r'ability to .+',
            r'knowledge of .+'
        ]
        
        for pattern in skill_patterns:
            matches = re.findall(pattern, job_description, re.IGNORECASE)
            phrases.extend(matches)
        
        return {
            "status": "success",
            "exact_phrases": phrases[:10],  # Top 10
            "message": "These phrases should be copied exactly to resume"
        }
        
    except Exception as e:
        return {"status": "error", "message": str(e)}

def extract_section_headers(job_description):
    """
    Extract section headers to mirror in resume structure.
    
    Args:
        job_description (str): Job posting text
    
    Returns:
        list: Section headers found
    """
    try:
        headers = []
        
        # Common header patterns
        header_patterns = [
            r'what you.?ll do',
            r'responsibilities',
            r'requirements',
            r'qualifications',
            r'skills',
            r'experience',
            r'key duties'
        ]
        
        for pattern in header_patterns:
            if re.search(pattern, job_description, re.IGNORECASE):
                headers.append(pattern.replace('you.?ll', 'you will'))
        
        return {
            "status": "success", 
            "headers": headers,
            "message": "Use these headers to structure resume sections"
        }
        
    except Exception as e:
        return {"status": "error", "message": str(e)}

def analyze_job_posting(job_description):
    """
    Complete analysis of job posting.
    
    Args:
        job_description (str): Full job posting text
    
    Returns:
        dict: Complete analysis results
    """
    return {
        "keywords": extract_keywords(job_description),
        "exact_phrases": find_exact_phrases(job_description), 
        "section_headers": extract_section_headers(job_description),
        "recommendation": "Feed this analysis to your AI along with docs/agent-instructions.md"
    }

# Example usage
if __name__ == "__main__":
    print("Job Description Analyzer")
    print("Extracts keywords using Uchenna's methodology")
    print("Use with AI for complete resume tailoring")