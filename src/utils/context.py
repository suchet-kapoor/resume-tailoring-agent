"""
Context and Planning Module

Gathers user inputs and creates a detailed execution plan for the subagent.
Coordinates the overall workflow before delegating to subagent.
"""

from pathlib import Path
import json
from datetime import datetime


class ContextGatherer:
    """Collects and organizes user inputs for resume tailoring."""
    
    def __init__(self):
        self.resume_file = None
        self.job_description = None
        self.user_profile = {}
        self.execution_plan = {}
    
    def gather_resume_input(self, file_path: str) -> dict:
        """
        Validate and load resume file.
        
        Args:
            file_path (str): Path to resume file (.pdf, .docx, .txt)
        
        Returns:
            dict: Status and file information
        """
        try:
            path = Path(file_path)
            
            if not path.exists():
                return {"status": "error", "message": f"File not found: {file_path}"}
            
            if path.suffix.lower() not in ['.pdf', '.docx', '.doc', '.txt']:
                return {"status": "error", "message": "Unsupported file format. Use .pdf, .docx, or .txt"}
            
            if path.stat().st_size == 0:
                return {"status": "error", "message": "File is empty"}
            
            self.resume_file = str(path.absolute())
            
            return {
                "status": "success",
                "file_path": str(path),
                "file_name": path.name,
                "file_size": path.stat().st_size,
                "file_type": path.suffix.lower()
            }
        
        except Exception as e:
            return {"status": "error", "message": f"Failed to process resume file: {str(e)}"}
    
    def gather_job_description(self, job_text: str) -> dict:
        """
        Validate and store job description.
        
        Args:
            job_text (str): The job description text
        
        Returns:
            dict: Validation status
        """
        if not job_text or len(job_text.strip()) < 100:
            return {
                "status": "error",
                "message": "Job description too short (minimum 100 characters)"
            }
        
        self.job_description = job_text.strip()
        
        return {
            "status": "success",
            "text_length": len(job_text),
            "character_count": len(job_text),
            "word_count": len(job_text.split())
        }
    
    def gather_user_preferences(self, preferences: dict = None) -> dict:
        """
        Gather optional user preferences for tailoring.
        
        Args:
            preferences (dict): Optional custom preferences
                - emphasis_areas: List of areas to emphasize
                - tone: Professional/Casual/Technical
                - include_cover_letter: bool
                - max_length: str (one-page, two-page)
        
        Returns:
            dict: Validated preferences
        """
        defaults = {
            "emphasis_areas": [],
            "tone": "professional",
            "include_cover_letter": False,
            "max_length": "one-page",
            "keywords_priority": "high",
            "ats_optimization": True
        }
        
        if preferences:
            defaults.update(preferences)
        
        self.user_profile = defaults
        
        return {"status": "success", "preferences": defaults}
    
    def create_execution_plan(self) -> dict:
        """
        Create a detailed execution plan based on gathered inputs.
        
        Returns:
            dict: Structured execution plan for subagent
        """
        if not self.resume_file or not self.job_description:
            return {
                "status": "error",
                "message": "Resume file and job description are required"
            }
        
        plan = {
            "execution_id": f"plan_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "timestamp": datetime.now().isoformat(),
            "workflow_stages": [
                {
                    "stage": 1,
                    "name": "Parse Resume",
                    "description": "Extract candidate information from resume file",
                    "inputs": {
                        "file_path": self.resume_file,
                        "file_type": Path(self.resume_file).suffix.lower()
                    },
                    "expected_output": {
                        "name": "string",
                        "email": "string",
                        "phone": "string",
                        "professional_summary": "string",
                        "skills": "list",
                        "experience": "list of objects",
                        "education": "list of objects"
                    }
                },
                {
                    "stage": 2,
                    "name": "Analyze Job Description",
                    "description": "Extract requirements, keywords, and priorities from job posting",
                    "inputs": {
                        "job_description": self.job_description[:500] + "..."  # First 500 chars
                    },
                    "expected_output": {
                        "key_requirements": "list",
                        "technical_skills": "list",
                        "soft_skills": "list",
                        "keywords": "list",
                        "role_title": "string",
                        "job_level": "string"
                    }
                },
                {
                    "stage": 3,
                    "name": "Match and Tailor",
                    "description": "Align resume with job description using keyword matching strategy",
                    "matching_strategy": "verbatim_keyword_matching",
                    "tactics": [
                        "Copy exact phrases from job description",
                        "Mirror job description structure",
                        "Restructure experience to match requirements",
                        "Highlight relevant skills first",
                        "Quantify achievements where possible"
                    ],
                    "inputs": {
                        "parsed_resume": "from stage 1",
                        "job_analysis": "from stage 2",
                        "user_preferences": self.user_profile
                    },
                    "expected_output": {
                        "tailored_resume": "complete resume object",
                        "changes_made": "list of modifications",
                        "keyword_coverage": "percentage"
                    }
                },
                {
                    "stage": 4,
                    "name": "Validate",
                    "description": "Run comprehensive validation checks",
                    "validation_checks": [
                        "keyword_matching (target: 70%+)",
                        "format_compliance (ATS requirements)",
                        "content_consistency (no conflicts)",
                        "completeness (all fields filled)"
                    ],
                    "inputs": {
                        "tailored_resume": "from stage 3",
                        "job_description": self.job_description
                    },
                    "expected_output": {
                        "validation_status": "passed/review_recommended",
                        "score": "number 0-100",
                        "issues": "list",
                        "recommendations": "list"
                    }
                },
                {
                    "stage": 5,
                    "name": "Generate Output",
                    "description": "Create .docx file from tailored resume",
                    "inputs": {
                        "tailored_resume": "from stage 3",
                        "output_directory": "project root"
                    },
                    "expected_output": {
                        "file_path": "path to generated .docx",
                        "file_name": "filename",
                        "status": "success/error"
                    }
                }
            ],
            "user_preferences": self.user_profile,
            "success_criteria": {
                "keyword_coverage_minimum": "70%",
                "validation_status": "passed",
                "file_generated": True,
                "no_critical_errors": True
            },
            "estimated_time": "2-3 minutes"
        }
        
        self.execution_plan = plan
        return {"status": "success", "plan": plan}
    
    def get_summary(self) -> dict:
        """Get a summary of gathered inputs and plan."""
        return {
            "resume_file": self.resume_file,
            "job_description_length": len(self.job_description) if self.job_description else 0,
            "user_preferences": self.user_profile,
            "plan_created": bool(self.execution_plan),
            "execution_id": self.execution_plan.get('execution_id') if self.execution_plan else None
        }
    
    def export_context(self, output_file: str = None) -> dict:
        """
        Export the complete context as JSON for subagent.
        
        Args:
            output_file (str): Optional file path to save context
        
        Returns:
            dict: Context data
        """
        context = {
            "execution_id": self.execution_plan.get('execution_id'),
            "resume_file": self.resume_file,
            "job_description": self.job_description,
            "user_preferences": self.user_profile,
            "workflow": self.execution_plan.get('workflow_stages', []),
            "success_criteria": self.execution_plan.get('success_criteria', {})
        }
        
        if output_file:
            try:
                with open(output_file, 'w') as f:
                    json.dump(context, f, indent=2)
                return {
                    "status": "success",
                    "message": "Context exported",
                    "file_path": output_file
                }
            except Exception as e:
                return {
                    "status": "error",
                    "message": f"Failed to export context: {str(e)}"
                }
        
        return {"status": "success", "context": context}
