#!/usr/bin/env python3
"""
Resume Tailoring Agent - Main Entry Point

Orchestrates the resume tailoring workflow:
1. Gathers user inputs (resume + job description)
2. Creates execution plan with detailed context
3. Delegates work to subagent for processing
4. Generates tailored resume in .docx format
5. Validates output before returning

Based on Uchenna's proven ATS-beating methodology.
"""

import sys
import os
from pathlib import Path
import json

# Add utils to path
sys.path.insert(0, str(Path(__file__).parent))

from utils.context import ContextGatherer
from utils.validation import ResumeValidator
from utils.resume_generator import generate_docx_resume


class ResumeTailoringAgent:
    """Main orchestration agent for resume tailoring workflow."""
    
    def __init__(self):
        self.context_gatherer = ContextGatherer()
        self.validator = ResumeValidator()
        self.execution_status = {}
    
    def run_workflow(self, resume_file_path: str, job_description: str, 
                     preferences: dict = None, output_dir: str = None) -> dict:
        """
        Main workflow orchestration.
        
        Args:
            resume_file_path (str): Path to resume file
            job_description (str): Job description text
            preferences (dict): User preferences (optional)
            output_dir (str): Output directory (defaults to project root)
        
        Returns:
            dict: Workflow result with tailored resume file path
        """
        print("\n🎯 Resume Tailoring Agent - Starting Workflow\n")
        
        # ============ PHASE 1: CONTEXT GATHERING ============
        print("📋 Phase 1: Gathering context...")
        
        # Step 1a: Validate resume file
        resume_check = self.context_gatherer.gather_resume_input(resume_file_path)
        if resume_check["status"] == "error":
            return {"status": "error", "phase": 1, "message": resume_check["message"]}
        print(f"   ✓ Resume loaded: {resume_check['file_name']}")
        
        # Step 1b: Validate job description
        job_check = self.context_gatherer.gather_job_description(job_description)
        if job_check["status"] == "error":
            return {"status": "error", "phase": 1, "message": job_check["message"]}
        print(f"   ✓ Job description received ({job_check['word_count']} words)")
        
        # Step 1c: Gather preferences
        self.context_gatherer.gather_user_preferences(preferences)
        print("   ✓ User preferences set")
        
        # ============ PHASE 2: EXECUTION PLANNING ============
        print("\n📊 Phase 2: Creating execution plan...")
        plan_result = self.context_gatherer.create_execution_plan()
        if plan_result["status"] == "error":
            return {"status": "error", "phase": 2, "message": plan_result["message"]}
        
        execution_plan = plan_result["plan"]
        execution_id = execution_plan["execution_id"]
        print(f"   ✓ Plan created (ID: {execution_id})")
        print(f"   ✓ {len(execution_plan['workflow_stages'])} workflow stages defined")
        
        # ============ PHASE 3: SUBAGENT DELEGATION ============
        print("\n🤖 Phase 3: Delegating to subagent...")
        print(f"   Execution ID: {execution_id}")
        
        subagent_context = self.context_gatherer.export_context()
        subagent_result = self._delegate_to_subagent(
            execution_id=execution_id,
            context=subagent_context["context"],
            execution_plan=execution_plan
        )
        
        if subagent_result["status"] == "error":
            return {"status": "error", "phase": 3, "message": subagent_result["message"]}
        
        tailored_resume_data = subagent_result.get("tailored_resume", {})
        print(f"   ✓ Subagent completed processing")
        
        # ============ PHASE 4: VALIDATION ============
        print("\n✅ Phase 4: Validating tailored resume...")
        
        resume_text = self._convert_to_text(tailored_resume_data)
        validation_result = self.validator.validate_all(
            resume_data=tailored_resume_data,
            job_description=job_description,
            tailored_resume_text=resume_text
        )
        
        print(f"   ✓ Validation Score: {validation_result['overall_score']}/100")
        print(f"   ✓ Keyword Match: {validation_result['keyword_validation']['keyword_match_percentage']}%")
        print(f"   ✓ Format Status: {validation_result['format_validation']['status']}")
        
        if validation_result['total_errors'] > 0:
            print(f"   ⚠ Issues found: {validation_result['total_errors']}")
        
        # ============ PHASE 5: OUTPUT GENERATION ============
        print("\n💾 Phase 5: Generating .docx output...")
        
        if output_dir is None:
            output_dir = str(Path(__file__).parent.parent)  # Project root
        
        output_result = generate_docx_resume(
            resume_data=tailored_resume_data,
            output_dir=output_dir
        )
        
        if output_result["status"] == "error":
            return {"status": "error", "phase": 5, "message": output_result["message"]}
        
        print(f"   ✓ Resume generated: {output_result['file_name']}")
        print(f"   ✓ Location: {output_result['file_path']}")
        
        # ============ WORKFLOW COMPLETE ============
        print("\n" + "="*50)
        print("✨ WORKFLOW COMPLETED SUCCESSFULLY!")
        print("="*50 + "\n")
        
        return {
            "status": "success",
            "execution_id": execution_id,
            "output_file": output_result["file_path"],
            "output_file_name": output_result["file_name"],
            "validation": {
                "score": validation_result["overall_score"],
                "status": validation_result["overall_status"],
                "keyword_match": validation_result["keyword_validation"]["keyword_match_percentage"]
            },
            "changes_made": subagent_result.get("changes_made", []),
            "warnings": self.validator.warnings,
            "errors": self.validator.errors
        }
    
    def _delegate_to_subagent(self, execution_id: str, context: dict, 
                              execution_plan: dict) -> dict:
        """
        Delegate work to subagent for resume tailoring.
        
        This would integrate with your subagent orchestration system.
        For now, it simulates the work and returns a structured result.
        
        Args:
            execution_id (str): Unique execution ID
            context (dict): Full execution context
            execution_plan (dict): Detailed workflow plan
        
        Returns:
            dict: Subagent results with tailored resume
        """
        print(f"   Calling subagent for execution: {execution_id}")
        
        # In production, this would:
        # 1. Call your subagent orchestration system
        # 2. Pass the execution_plan and context
        # 3. Subagent would handle all 5 workflow stages
        # 4. Return structured results
        
        # For now, simulate with placeholder
        try:
            # This is where the subagent takes over:
            # - Parses the resume from context["resume_file"]
            # - Analyzes job description from context["job_description"]
            # - Performs keyword matching and tailoring
            # - Validates output
            # 
            # Expected to return a tailored_resume object
            
            print("   ⏳ Subagent processing stages 1-4...")
            
            # Placeholder result structure
            tailored_resume = {
                "name": "Candidate Name",
                "email": "email@example.com",
                "phone": "+1-555-0123",
                "summary": "Professional summary tailored to job requirements...",
                "skills": ["Skill 1", "Skill 2", "Skill 3"],
                "experience": [
                    {
                        "title": "Relevant Job Title",
                        "company": "Company Name",
                        "start_date": "2023",
                        "end_date": "2024",
                        "description": "Description tailored with keywords from job posting"
                    }
                ],
                "education": [
                    {
                        "degree": "Degree",
                        "field": "Field of Study",
                        "school": "University Name",
                        "graduation_date": "2023"
                    }
                ]
            }
            
            return {
                "status": "success",
                "execution_id": execution_id,
                "tailored_resume": tailored_resume,
                "changes_made": [
                    "Aligned job title with job posting",
                    "Added relevant keywords from job description",
                    "Reorganized experience to match job requirements",
                    "Enhanced skills section with posting keywords"
                ]
            }
        
        except Exception as e:
            return {
                "status": "error",
                "message": f"Subagent processing failed: {str(e)}"
            }
    
    @staticmethod
    def _convert_to_text(resume_data: dict) -> str:
        """Convert resume data structure to plain text."""
        parts = []
        
        if resume_data.get('name'):
            parts.append(resume_data['name'])
        if resume_data.get('email'):
            parts.append(resume_data['email'])
        if resume_data.get('summary'):
            parts.append(resume_data['summary'])
        
        if resume_data.get('skills'):
            parts.append(' '.join(resume_data['skills']))
        
        for job in resume_data.get('experience', []):
            if job.get('title'):
                parts.append(job['title'])
            if job.get('company'):
                parts.append(job['company'])
            if job.get('description'):
                parts.append(job['description'])
        
        for edu in resume_data.get('education', []):
            if edu.get('degree'):
                parts.append(edu['degree'])
            if edu.get('school'):
                parts.append(edu['school'])
        
        return ' '.join(parts)


def main():
    """CLI entry point."""
    print("🎯 Resume Tailoring Agent")
    print("=" * 50)
    print()
    
    # Example usage (in production, would read from user input or API)
    resume_file = input("Enter path to resume file: ").strip()
    
    if not resume_file or not Path(resume_file).exists():
        print("❌ Resume file not found")
        return
    
    print("\nPaste job description (press Enter twice when done):")
    lines = []
    empty_lines = 0
    while True:
        line = input()
        if line == "":
            empty_lines += 1
            if empty_lines >= 2:
                break
        else:
            empty_lines = 0
            lines.append(line)
    
    job_description = "\n".join(lines)
    
    if not job_description.strip():
        print("❌ Job description is required")
        return
    
    # Run the workflow
    agent = ResumeTailoringAgent()
    result = agent.run_workflow(
        resume_file_path=resume_file,
        job_description=job_description,
        preferences={"tone": "professional", "ats_optimization": True}
    )
    
    if result["status"] == "success":
        print("\n✅ Output file:")
        print(f"   {result['output_file']}")
    else:
        print(f"\n❌ Error: {result['message']}")


if __name__ == "__main__":
    main()