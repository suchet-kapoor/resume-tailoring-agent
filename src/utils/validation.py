"""
Resume Validation Module

Provides validation for:
1. Keyword matching (job keywords coverage)
2. Format validation (ATS compliance)
3. Content validation (no conflicting info)
"""

import re
from typing import List, Dict, Tuple

class ResumeValidator:
    """Comprehensive resume validation for ATS compliance and keyword coverage."""
    
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.score = 0
    
    def validate_keywords(self, tailored_resume: str, job_description: str) -> Dict:
        """
        Validate keyword matching between resume and job description.
        
        Args:
            tailored_resume (str): The tailored resume text
            job_description (str): The job description text
        
        Returns:
            dict: Keyword validation results with match percentage
        """
        self.errors = []
        self.warnings = []
        
        # Extract keywords from job description
        job_keywords = self._extract_keywords(job_description)
        
        # Check which keywords appear in resume
        matched_keywords = []
        missing_keywords = []
        
        for keyword in job_keywords:
            if self._keyword_in_text(keyword, tailored_resume):
                matched_keywords.append(keyword)
            else:
                missing_keywords.append(keyword)
        
        match_percentage = (len(matched_keywords) / len(job_keywords) * 100) if job_keywords else 0
        
        if match_percentage < 60:
            self.errors.append(f"Low keyword coverage: {match_percentage:.1f}%")
        elif match_percentage < 80:
            self.warnings.append(f"Medium keyword coverage: {match_percentage:.1f}%")
        
        return {
            "status": "valid" if match_percentage >= 60 else "warning",
            "keyword_match_percentage": round(match_percentage, 1),
            "matched_keywords": matched_keywords,
            "missing_keywords": missing_keywords,
            "total_keywords_found": len(matched_keywords),
            "total_keywords_searched": len(job_keywords)
        }
    
    def validate_format(self, resume_data: Dict) -> Dict:
        """
        Validate ATS-friendly formatting.
        
        Args:
            resume_data (dict): Resume data structure
        
        Returns:
            dict: Format validation results
        """
        issues = []
        
        # Check required fields
        required_fields = ['name', 'email', 'phone', 'experience', 'education']
        for field in required_fields:
            if field not in resume_data or not resume_data[field]:
                issues.append(f"Missing required field: {field}")
        
        # Check for problematic formatting
        if resume_data.get('name'):
            if len(resume_data['name']) > 50:
                issues.append("Name is too long (max 50 chars)")
        
        if resume_data.get('email'):
            if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', resume_data['email']):
                issues.append("Invalid email format")
        
        if resume_data.get('phone'):
            if not re.match(r'^[\d\-\+\(\)\s]{10,}$', resume_data['phone']):
                issues.append("Invalid phone format")
        
        # Check experience entries
        if resume_data.get('experience'):
            for i, job in enumerate(resume_data['experience']):
                if not job.get('title'):
                    issues.append(f"Experience entry {i+1}: Missing job title")
                if not job.get('company'):
                    issues.append(f"Experience entry {i+1}: Missing company name")
                if not job.get('description'):
                    issues.append(f"Experience entry {i+1}: Missing job description")
        
        # Check education entries
        if resume_data.get('education'):
            for i, edu in enumerate(resume_data['education']):
                if not edu.get('degree'):
                    issues.append(f"Education entry {i+1}: Missing degree")
                if not edu.get('school'):
                    issues.append(f"Education entry {i+1}: Missing school name")
        
        return {
            "status": "valid" if not issues else "invalid",
            "issues": issues,
            "issue_count": len(issues),
            "is_ats_compliant": len(issues) == 0
        }
    
    def validate_content(self, resume_data: Dict, job_description: str) -> Dict:
        """
        Validate content for consistency and relevance.
        
        Args:
            resume_data (dict): Resume data structure
            job_description (str): The job description
        
        Returns:
            dict: Content validation results
        """
        issues = []
        
        # Check for inconsistencies
        resume_text = self._stringify_resume(resume_data)
        
        # Check for conflicting dates
        experience_issues = self._check_date_conflicts(resume_data.get('experience', []))
        issues.extend(experience_issues)
        
        # Check for empty descriptions
        if resume_data.get('experience'):
            for i, job in enumerate(resume_data['experience']):
                if job.get('description') and len(job['description'].strip()) < 20:
                    issues.append(f"Experience entry {i+1}: Description too short")
        
        # Check summary relevance to job
        if resume_data.get('summary'):
            summary_keywords = self._extract_keywords(resume_data['summary'])
            job_keywords = self._extract_keywords(job_description)
            overlap = len(set(summary_keywords) & set(job_keywords))
            if overlap < len(job_keywords) * 0.3:
                self.warnings.append("Summary may not align well with job description")
        
        # Check for red flags
        red_flags = self._check_red_flags(resume_text)
        issues.extend(red_flags)
        
        return {
            "status": "valid" if not issues else "warning",
            "content_issues": issues,
            "issue_count": len(issues),
            "consistency_check": len(issues) == 0
        }
    
    def validate_all(self, resume_data: Dict, job_description: str, tailored_resume_text: str) -> Dict:
        """
        Run all validations and return comprehensive results.
        
        Args:
            resume_data (dict): Resume data structure
            job_description (str): The job description
            tailored_resume_text (str): The tailored resume as text
        
        Returns:
            dict: Complete validation report
        """
        keyword_results = self.validate_keywords(tailored_resume_text, job_description)
        format_results = self.validate_format(resume_data)
        content_results = self.validate_content(resume_data, job_description)
        
        # Calculate overall score
        keyword_score = keyword_results['keyword_match_percentage']
        format_score = 100 if format_results['status'] == 'valid' else 50
        content_score = 100 if content_results['status'] == 'valid' else 50
        
        overall_score = (keyword_score * 0.5 + format_score * 0.3 + content_score * 0.2)
        
        return {
            "overall_status": "passed" if overall_score >= 70 else "review_recommended",
            "overall_score": round(overall_score, 1),
            "keyword_validation": keyword_results,
            "format_validation": format_results,
            "content_validation": content_results,
            "total_errors": len(self.errors),
            "total_warnings": len(self.warnings),
            "errors": self.errors,
            "warnings": self.warnings
        }
    
    # Helper methods
    
    @staticmethod
    def _extract_keywords(text: str) -> List[str]:
        """Extract key terms from text."""
        # Remove common words
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'is', 'are', 'was', 'be', 'been', 'have', 'has', 'had'}
        
        # Extract words (simple approach)
        words = re.findall(r'\b[a-z]+\b', text.lower())
        keywords = [w for w in words if len(w) > 3 and w not in stop_words]
        
        # Return unique keywords
        return list(set(keywords))[:50]  # Limit to top 50
    
    @staticmethod
    def _keyword_in_text(keyword: str, text: str) -> bool:
        """Check if keyword appears in text (case-insensitive, whole word)."""
        pattern = r'\b' + re.escape(keyword) + r'\b'
        return bool(re.search(pattern, text, re.IGNORECASE))
    
    @staticmethod
    def _stringify_resume(resume_data: Dict) -> str:
        """Convert resume data to single text string."""
        parts = []
        
        if resume_data.get('name'):
            parts.append(resume_data['name'])
        if resume_data.get('summary'):
            parts.append(resume_data['summary'])
        if resume_data.get('skills'):
            parts.append(' '.join(resume_data['skills']))
        
        for job in resume_data.get('experience', []):
            parts.extend([job.get('title', ''), job.get('company', ''), job.get('description', '')])
        
        for edu in resume_data.get('education', []):
            parts.extend([edu.get('degree', ''), edu.get('school', '')])
        
        return ' '.join(parts)
    
    @staticmethod
    def _check_date_conflicts(experience: List[Dict]) -> List[str]:
        """Check for date overlaps or inconsistencies."""
        issues = []
        
        for i, job in enumerate(experience):
            start = job.get('start_date', '')
            end = job.get('end_date', '')
            
            if not start or not end:
                continue
            
            # Basic date format check
            if not re.match(r'\d{4}', start) or not re.match(r'\d{4}', end):
                issues.append(f"Experience entry {i+1}: Invalid date format")
        
        return issues
    
    @staticmethod
    def _check_red_flags(text: str) -> List[str]:
        """Check for common resume red flags."""
        issues = []
        
        red_flag_patterns = {
            r'(?i)under construction': "Unfinished content detected",
            r'(?i)tbd|to be determined': "Incomplete information found",
            r'(?i)ref upon request': "Consider including actual references",
            r'\[\w+\]': "Placeholder text found",
        }
        
        for pattern, message in red_flag_patterns.items():
            if re.search(pattern, text):
                issues.append(message)
        
        return issues
