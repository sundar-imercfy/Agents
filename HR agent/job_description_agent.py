#!/usr/bin/env python3
"""
Job Description Agent - Clean Implementation
Generates comprehensive job descriptions using OpenAI GPT models
"""

import os
from typing import Optional, List
from pydantic import BaseModel
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from dotenv import load_dotenv

# Import OpenAI directly to avoid LangChain compatibility issues
import openai

# Load environment variables
load_dotenv()

class JobDescription(BaseModel):
    """Structured job description model"""
    job_title: str
    department: str
    experience_level: str
    location: str
    salary_range: str
    job_summary: str
    key_responsibilities: List[str]
    required_skills: List[str]
    preferred_skills: List[str]
    education: str
    benefits: List[str]
    company_culture: str

class JobDescriptionAgent:
    """AI-powered job description generator"""
    
    def __init__(self, model_name: str = "gpt-4o-mini"):
        """Initialize the agent with specified model"""
        self.model_name = model_name
        self.organization_context = ""
        
        # Set OpenAI API key
        openai.api_key = os.getenv("OPENAI_API_KEY")
        if not openai.api_key:
            raise ValueError("OpenAI API key not found in environment variables")
        
    def set_organization_context(self, organization: str):
        """Set organization context for customized descriptions"""
        # Simple organization contexts for basic customization
        org_contexts = {
            "Technology Company": "A leading technology company focused on innovation and cutting-edge solutions.",
            "Consulting Firm": "A professional consulting firm helping businesses achieve their goals.",
            "Startup": "A dynamic startup fostering creativity and entrepreneurship.",
            "Enterprise": "A large enterprise organization with established processes and growth opportunities."
        }
        self.organization_context = org_contexts.get(organization, "")
    
    def generate_job_description(self, job_input: str, temperature: float = 0.7) -> Optional[JobDescription]:
        """Generate a comprehensive job description from simple input"""
        
        # Create the prompt
        org_context = f"Company Context: {self.organization_context}" if self.organization_context else ""
        
        prompt = f"""
You are an expert HR professional. Create a comprehensive, professional job description based on the input provided.

{org_context}

Job Input: {job_input}

Generate a detailed job description in JSON format with exactly these fields:
- job_title: Professional, specific title
- department: Relevant department
- experience_level: Entry Level, Mid-Level, Senior, or Executive
- location: Include remote/hybrid options when appropriate
- salary_range: Realistic range based on role and experience
- job_summary: 2-3 sentences describing the role
- key_responsibilities: Array of 5-7 specific, actionable responsibilities
- required_skills: Array of 5-8 essential skills and qualifications
- preferred_skills: Array of 3-5 bonus qualifications
- education: Degree requirements or equivalent experience
- benefits: Array of 4-6 attractive benefits and perks
- company_culture: Description of work environment and values

Make the description inclusive, professional, and appealing to qualified candidates.

Return only valid JSON format.
"""
        
        try:
            # Use OpenAI directly
            client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            
            response = client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": "You are an expert HR professional. Always respond with valid JSON format."},
                    {"role": "user", "content": prompt}
                ],
                temperature=temperature,
                max_tokens=2000
            )
            
            # Parse the JSON response
            import json
            result_text = response.choices[0].message.content.strip()
            
            # Clean up the response if it has markdown formatting
            if result_text.startswith("```json"):
                result_text = result_text.replace("```json", "").replace("```", "").strip()
            
            result_data = json.loads(result_text)
            
            # Create JobDescription object
            job_desc = JobDescription(**result_data)
            return job_desc
            
        except Exception as e:
            print(f"Error generating job description: {e}")
            return None
    
    def format_job_description(self, job_desc: JobDescription) -> str:
        """Format job description as markdown"""
        
        formatted = f"""
# {job_desc.job_title}

**Department:** {job_desc.department}  
**Experience Level:** {job_desc.experience_level}  
**Location:** {job_desc.location}  
**Salary Range:** {job_desc.salary_range}

## Job Summary
{job_desc.job_summary}

## Key Responsibilities
"""
        
        for i, responsibility in enumerate(job_desc.key_responsibilities, 1):
            formatted += f"{i}. {responsibility}\n"
        
        formatted += f"""
## Required Skills
"""
        for skill in job_desc.required_skills:
            formatted += f"• {skill}\n"
        
        formatted += f"""
## Preferred Skills
"""
        for skill in job_desc.preferred_skills:
            formatted += f"• {skill}\n"
        
        formatted += f"""
## Education
{job_desc.education}

## Benefits
"""
        for benefit in job_desc.benefits:
            formatted += f"• {benefit}\n"
        
        formatted += f"""
## Company Culture
{job_desc.company_culture}
"""
        
        return formatted.strip()

def main():
    """Command line interface for the job description agent"""
    print("🤖 Job Description Agent")
    print("=" * 50)
    
    # Check API key
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ OPENAI_API_KEY not found in environment variables.")
        print("Please set your OpenAI API key in the .env file.")
        return
    
    agent = JobDescriptionAgent()
    
    while True:
        print("\n" + "-" * 50)
        job_input = input("Enter job description (or 'quit' to exit): ").strip()
        
        if job_input.lower() in ['quit', 'exit', 'q']:
            break
        
        if not job_input:
            print("Please enter a job description.")
            continue
        
        print("\n🔄 Generating job description...")
        
        try:
            job_desc = agent.generate_job_description(job_input)
            
            if job_desc:
                print("\n✅ Job description generated successfully!")
                formatted_output = agent.format_job_description(job_desc)
                print("\n" + formatted_output)
                
                # Save to file
                filename = f"job_description_{job_desc.job_title.lower().replace(' ', '_')}.md"
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(formatted_output)
                print(f"\n💾 Saved to: {filename}")
            else:
                print("❌ Failed to generate job description.")
                
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n👋 Thank you for using Job Description Agent!")

if __name__ == "__main__":
    main()
