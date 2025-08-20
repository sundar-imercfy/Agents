import os
from typing import Dict, Any, Optional
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from openai import OpenAI
import json
from knowledge_base import KnowledgeBase

# Load environment variables
load_dotenv()

class JobDescription(BaseModel):
    """Structured output for job description"""
    job_title: str = Field(description="The official job title")
    department: str = Field(description="Department where the position belongs")
    experience_level: str = Field(description="Experience level required")
    job_summary: str = Field(description="Brief overview of the role")
    key_responsibilities: list = Field(description="List of main job responsibilities")
    required_skills: list = Field(description="List of required technical and soft skills")
    preferred_skills: list = Field(description="List of preferred but not required skills")
    education: str = Field(description="Educational requirements")
    location: str = Field(description="Job location (remote, hybrid, on-site)")
    salary_range: str = Field(description="Expected salary range")
    benefits: list = Field(description="List of benefits offered")
    company_culture: str = Field(description="Brief description of company culture and values")

class JobDescriptionAgent:
    def __init__(self, model_name: str = "gpt-4o-mini", temperature: float = 0.7):
        """Initialize the job description agent"""
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY is not set")
        self.client = OpenAI(api_key=api_key)
        self.model_name = model_name
        self.temperature = temperature

        self.output_parser = PydanticOutputParser(pydantic_object=JobDescription)
        self.knowledge_base = KnowledgeBase()
        
        # Create the prompt template
        self.prompt = PromptTemplate(
            template="""You are an expert HR professional and job description writer. 
            Create a comprehensive, professional job description based on the following input: {job_input}
            
            {organization_context}
            
            Please generate a detailed job description that includes all the required fields.
            Make sure the job description is:
            - Professional and engaging
            - Specific to the role and experience level
            - Inclusive and welcoming to diverse candidates
            - Realistic in terms of requirements and expectations
            - Aligned with current industry standards
            - Tailored to the specific organization's culture, values, and requirements
            
            {format_instructions}
            
            IMPORTANT: Return only valid JSON matching the schema. Do not include any extra text.
            
            Job Input: {job_input}""",
            input_variables=["job_input", "organization_context"],
            partial_variables={"format_instructions": self.output_parser.get_format_instructions()}
        )
    
    def generate_job_description(self, job_input: str, organization_id: Optional[str] = None) -> Optional[JobDescription]:
        """Generate a job description from the input with optional organization context"""
        try:
            # Get organization context if provided
            organization_context = ""
            if organization_id:
                # Extract role and experience level from input
                role, experience_level = self._extract_role_and_level(job_input)
                context = self.knowledge_base.get_job_context(organization_id, role, experience_level)
                organization_context = self._format_organization_context(context)
            
            # If no organization context, use default
            if not organization_context:
                organization_context = "Generate a general job description without specific company details."
            
            # Build prompt text
            prompt_text = self.prompt.format(
                job_input=job_input,
                organization_context=organization_context
            )
            
            # Call OpenAI Chat Completions
            response = self.client.chat.completions.create(
                model=self.model_name,
                temperature=self.temperature,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that returns only JSON."},
                    {"role": "user", "content": prompt_text}
                ]
            )
            content = response.choices[0].message.content if response.choices else ""
            if not content:
                return None
            
            # Parse to Pydantic model
            return self.output_parser.parse(content)
        except Exception as e:
            print(f"Error generating job description: {e}")
            return None
    
    def _extract_role_and_level(self, job_input: str) -> tuple[str, str]:
        """Extract role and experience level from job input"""
        input_lower = job_input.lower()
        
        # Common experience level keywords
        experience_keywords = {
            "entry": ["entry", "entry level", "junior", "fresh", "new graduate"],
            "mid": ["mid", "mid level", "intermediate", "experienced"],
            "senior": ["senior", "senior level", "lead", "principal"],
            "executive": ["executive", "director", "vp", "head", "chief"]
        }
        
        # Determine experience level
        experience_level = "mid"  # default
        for level, keywords in experience_keywords.items():
            if any(keyword in input_lower for keyword in keywords):
                experience_level = level
                break
        
        # Extract role (simplified)
        role = job_input.split()[0] if job_input else "developer"
        
        return role, experience_level
    
    def _format_organization_context(self, context: Dict[str, Any]) -> str:
        """Format organization context for the prompt"""
        if not context:
            return ""
        
        context_parts = []
        
        # Company information
        if context.get("company_name"):
            context_parts.append(f"Company: {context['company_name']}")
        if context.get("industry"):
            context_parts.append(f"Industry: {context['industry']}")
        if context.get("company_size"):
            context_parts.append(f"Company Size: {context['company_size']}")
        if context.get("location"):
            context_parts.append(f"Location: {context['location']}")
        
        # Culture and values
        if context.get("mission"):
            context_parts.append(f"Mission: {context['mission']}")
        if context.get("values"):
            context_parts.append(f"Company Values: {', '.join(context['values'])}")
        if context.get("work_style"):
            context_parts.append(f"Work Style: {context['work_style']}")
        
        # Benefits and compensation
        if context.get("salary_range"):
            context_parts.append(f"Salary Range: {context['salary_range']}")
        if context.get("benefits"):
            benefits = context['benefits']
            if benefits.get("health_insurance"):
                context_parts.append(f"Health Insurance: {benefits['health_insurance']}")
            if benefits.get("flexible_work"):
                context_parts.append(f"Work Arrangement: {benefits['flexible_work']}")
        
        # Technical context
        if context.get("tech_stack"):
            context_parts.append(f"Tech Stack: {', '.join(context['tech_stack'])}")
        if context.get("tools_platforms"):
            context_parts.append(f"Tools & Platforms: {', '.join(context['tools_platforms'])}")
        if context.get("certifications_preferred"):
            context_parts.append(f"Preferred Certifications: {', '.join(context['certifications_preferred'])}")
        
        # Department information
        if context.get("department_info"):
            dept = context['department_info']
            context_parts.append(f"Department: {dept.get('name', '')}")
            context_parts.append(f"Department Description: {dept.get('description', '')}")
        
        return "\n".join(context_parts)
    
    def format_job_description(self, job_desc: JobDescription) -> str:
        """Format the job description for display"""
        if not job_desc:
            return "Error: Could not generate job description"
        
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
        
        if job_desc.preferred_skills:
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
        return formatted

def main():
    """Main function to run the job description agent"""
    # Check if API key is set
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY not found in environment variables.")
        print("Please create a .env file with your OpenAI API key:")
        print("OPENAI_API_KEY=your_api_key_here")
        return
    
    # Initialize the agent
    agent = JobDescriptionAgent()
    
    print("🤖 Job Description Agent")
    print("=" * 50)
    print("Enter a job description request (e.g., 'web developer with 5 years experience')")
    print("Type 'quit' to exit")
    print()
    
    # Check for available organizations
    organizations = agent.knowledge_base.list_organizations()
    selected_org = None
    
    if organizations:
        print(f"\n📋 Available organizations: {', '.join(organizations)}")
        org_choice = input("Enter organization ID (or press Enter for general description): ").strip()
        if org_choice and org_choice in organizations:
            selected_org = org_choice
            print(f"✅ Using organization: {org_choice}")
        elif org_choice:
            print(f"❌ Organization '{org_choice}' not found. Using general description.")
    else:
        print("\n💡 No organizations in knowledge base. Run 'python knowledge_base_manager.py' to add organizations.")
    
    print()
    
    while True:
        try:
            user_input = input("Enter job description request: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("Goodbye! 👋")
                break
            
            if not user_input:
                print("Please enter a valid job description request.")
                continue
            
            print("\n🔄 Generating job description...")
            print()
            
            # Generate the job description
            job_desc = agent.generate_job_description(user_input, selected_org)
            
            if job_desc:
                # Display formatted output
                formatted_output = agent.format_job_description(job_desc)
                print(formatted_output)
                
                # Save to file option
                save_choice = input("\n💾 Save to file? (y/n): ").strip().lower()
                if save_choice in ['y', 'yes']:
                    filename = f"job_description_{job_desc.job_title.lower().replace(' ', '_')}.md"
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write(formatted_output)
                    print(f"✅ Job description saved to {filename}")

                # Upload to Google Docs option
                try:
                    upload_choice = input("\n🟢 Upload to Google Docs? (y/n): ").strip().lower()
                    if upload_choice in ['y', 'yes']:
                        from google_docs import upload_job_description_to_google_doc
                        doc_title = job_desc.job_title
                        doc_url = upload_job_description_to_google_doc(doc_title, formatted_output)
                        print(f"✅ Uploaded to Google Docs: {doc_url}")
                        print("Note: Adjust sharing settings in Google Drive if needed.")
                except Exception as ex:
                    print(f"❌ Google Docs upload failed: {ex}")
            else:
                print("❌ Failed to generate job description. Please try again.")
            
            print("\n" + "=" * 50 + "\n")
            
        except KeyboardInterrupt:
            print("\n\nGoodbye! 👋")
            break
        except Exception as e:
            print(f"❌ An error occurred: {e}")
            print("Please try again.")

if __name__ == "__main__":
    main()
