# 📚 **Complete Code Guide: HR Job Description Agent**
*Line-by-Line Code Tutorial for Prompt Engineers*

## 🎯 **Purpose of This Guide**
This document explains every single line of code in the HR Agent project in the simplest possible terms. It's designed for prompt engineers with limited coding knowledge who want to understand how each piece works.

## 📁 **Project Structure Overview**
```
HR agent_one/
├── streamlit_app.py           # Web interface (what users see)
├── job_description_agent.py   # AI brain (creates job descriptions)
├── knowledge_base.py          # Company data manager
├── demo.py                    # Example/test script
├── load_sample_data.py        # Loads sample companies
├── requirements.txt           # List of needed packages
├── start.bat                  # Windows startup script
├── env_example.txt           # Template for secret keys
├── README.md                 # Project documentation
└── knowledge_base/
    ├── organizations.json     # Sample company data
    └── job_templates.json     # Company type templates
```

---

## 📁 **File 1: `requirements.txt`** 
*This file lists all the external packages (libraries) the project needs*

```txt
langchain-core==0.3.20        # Core framework for building AI applications
langchain-openai==0.2.6       # Connects LangChain to OpenAI's models (GPT)
python-dotenv==1.0.1          # Loads secret keys from .env files
streamlit==1.37.1             # Creates the web interface (like a website)
openai==1.60.2                # Direct connection to OpenAI's API
google-api-python-client==2.149.0  # For Google Docs integration
google-auth-httplib2==0.2.0   # Google authentication
google-auth-oauthlib==1.2.1   # More Google authentication
```

**What it does:** Like a shopping list that tells Python which tools to download before the project can work.

**How to use it:** Run `pip install -r requirements.txt` to install everything at once.

---

## 📁 **File 2: `env_example.txt`**
*Template file showing what secret information you need*

```txt
# Line 1-2: Comments explaining what this section is for
# OpenAI API Configuration
# Get your API key from: https://platform.openai.com/api-keys

# Line 3: The actual secret key (you replace this with your real key)
OPENAI_API_KEY=your_api_key_here

# Line 5-8: Optional settings (commented out with #)
# Optional: Model Configuration  
# MODEL_NAME=gpt-3.5-turbo
# TEMPERATURE=0.7
```

**What each line does:**
- **Lines 1-2:** Comments (ignored by computer) explaining where to get API key
- **Line 3:** Where you put your real OpenAI API key
- **Lines 5-8:** Optional settings you can customize later

**What it does:** Shows you how to set up your secret OpenAI key. You copy this file, rename it to `.env`, and put your real key in it.

---

## 📁 **File 3: `start.bat`**
*Windows script to launch the application*

```batch
# Line 1: Don't show the commands being executed
@echo off                    

# Line 2: Display welcome message
echo Starting Job Description Agent...  

# Line 3: Empty line for better formatting
echo.                        

# Lines 4-7: Show checklist to user
echo Make sure you have:     
echo 1. Python installed
echo 2. Dependencies installed (pip install -r requirements.txt)
echo 3. OpenAI API key set in .env file

# Lines 8-10: More formatting and status
echo.                        
echo Starting Streamlit web interface...  
echo.

# Line 11: Actually start the web application
streamlit run streamlit_app.py           

# Line 12: Wait for user to press a key before closing window
pause                        
```

**What each line does:**
- **Line 1:** `@echo off` - Hides technical commands from user
- **Lines 2-10:** `echo` commands - Display helpful messages
- **Line 11:** `streamlit run streamlit_app.py` - Launches the web app
- **Line 12:** `pause` - Keeps window open until user presses a key

**What it does:** Like a "start button" for Windows that automatically launches the web application and shows helpful instructions.

---

## 📁 **File 4: `knowledge_base.py`**
*Manages company data and information storage*

### **Imports Section (Lines 1-6):**
```python
# Line 1: For reading and writing JSON files (data storage format)
import json                  

# Line 2: For file system operations (creating folders, checking files)
import os                    

# Line 3: Type hints - helps catch errors and makes code clearer
from typing import Dict, List, Optional, Any  

# Line 4: For timestamps (when was data last updated)
from datetime import datetime  

# Line 5: For creating structured data classes easily
from dataclasses import dataclass, asdict    

# Line 6: For handling file paths in a cross-platform way
from pathlib import Path     
```

### **Data Structure Classes (Lines 8-67):**

#### **CompanyInfo Class (Lines 8-17):**
```python
# Line 8: @dataclass makes this a structured data container
@dataclass
class CompanyInfo:           # Basic company details
    # Line 10: Required field - company name (must be text)
    name: str               
    # Line 11: Required field - what business they're in
    industry: str           
    # Line 12: Required field - how many employees (as text like "50-100")
    size: str              
    # Line 13: Required field - where company is located
    location: str          
    # Line 14: Optional field - when company was started (can be None)
    founded_year: Optional[int] = None  
    # Line 15: Optional field - company website (can be None)
    website: Optional[str] = None       
    # Line 16: Optional field - description of company (can be None)
    description: Optional[str] = None   
```

**What this class does:** Like a digital business card template that stores all the basic info about a company. Each company will have one of these filled out.

#### **CompanyCulture Class (Lines 19-27):**
```python
@dataclass
class CompanyCulture:        # Company values and work style
    # Line 21: Why the company exists (purpose statement)
    mission: str            
    # Line 22: What they want to achieve in the future
    vision: str             
    # Line 23: List of company values (like ["Innovation", "Teamwork"])
    values: List[str]       
    # Line 24: How they work (like "fast-paced" or "collaborative")
    work_style: str         
    # Line 25: Their diversity and inclusion policies
    diversity_inclusion: str 
    # Line 26: How they handle work-life balance
    work_life_balance: str  
```

**What this class does:** Captures the "personality" and culture of the company - how it feels to work there.

#### **BenefitsPackage Class (Lines 29-37):**
```python
@dataclass
class BenefitsPackage:       # What employees get beyond salary
    # Line 31: Health insurance details
    health_insurance: str
    # Line 32: 401k, pension plans, etc.
    retirement_plans: str
    # Line 33: Vacation, sick days, holidays
    paid_time_off: str
    # Line 34: Remote work, hybrid, office options
    flexible_work: str  
    # Line 35: Training, conferences, education budget
    professional_development: str
    # Line 36: Extra perks (gym, food, etc.) as a list
    additional_benefits: List[str]
```

#### **SalaryRanges Class (Lines 39-45):**
```python
@dataclass
class SalaryRanges:          # Pay scales by experience level
    # Line 41: Dictionary mapping job titles to salary ranges for new grads
    entry_level: Dict[str, str]  # Like {"developer": "$60k-80k"}
    # Line 42: Same but for 2-5 years experience
    mid_level: Dict[str, str]
    # Line 43: Same but for 5+ years experience  
    senior_level: Dict[str, str]
    # Line 44: Same but for executive/director level
    executive_level: Dict[str, str]
```

### **KnowledgeBase Main Class (Lines 69-311):**

#### **Initialization Method (Lines 72-79):**
```python
def __init__(self, data_dir: str = "knowledge_base"):
    # Line 73: Create Path object for data directory
    self.data_dir = Path(data_dir)          
    # Line 74: Create the directory if it doesn't exist
    self.data_dir.mkdir(exist_ok=True)      
    # Line 75: Set path for companies data file
    self.organizations_file = self.data_dir / "organizations.json"  
    # Line 76: Set path for job templates file
    self.templates_file = self.data_dir / "job_templates.json"      
    # Line 78: Set up the files if they don't exist yet
    self._initialize_files()                
```

**What this does:** Sets up the filing system for storing company information, like creating folders on your computer for organizing files.

#### **Key Methods Explained:**

**Adding a Company (Lines 114-130):**
```python
def add_organization(self, org_id: str, data: OrganizationalData) -> bool:
    try:                                    # Try to do this, catch errors
        # Line 117: Load existing companies from file
        organizations = self._load_organizations()
        
        # Line 119-120: Add timestamp showing when this was last updated
        data.last_updated = datetime.now().isoformat()
        
        # Line 122-123: Convert company data to dictionary format
        org_data = asdict(data)
        organizations[org_id] = org_data
        
        # Line 125: Save back to file
        self._save_organizations(organizations)
        return True                         # Success!
    except Exception as e:                  # If something went wrong
        print(f"Error adding organization: {e}")  # Show error message
        return False                        # Failed
```

**What this does:** Like adding a new contact to your phone - takes company information and saves it to the database.

**Getting Company Info (Lines 132-142):**
```python
def get_organization(self, org_id: str) -> Optional[OrganizationalData]:
    try:
        # Line 135: Load all companies from file
        organizations = self._load_organizations()
        # Line 136-137: Check if the company ID exists
        if org_id in organizations:
            org_data = organizations[org_id]
            # Line 138: Convert back to structured format and return
            return self._dict_to_organizational_data(org_data)
        return None                         # Company not found
    except Exception as e:
        print(f"Error retrieving organization: {e}")
        return None
```

**What this does:** Like looking up a contact by name in your phone - finds and returns company information.

**Getting Job Context (Lines 181-213):**
```python
def get_job_context(self, org_id: str, role: str, experience_level: str):
    try:
        # Line 184: Get the company data
        org_data = self.get_organization(org_id)
        if not org_data:
            return {}                       # No company found, return empty
        
        # Line 189: Get salary info for this specific role and level
        salary_range = self._get_salary_range(org_data.salary_ranges, role, experience_level)
        
        # Line 192: Get department info for this role
        department_info = self._get_department_info(org_data.departments, role)
        
        # Line 194-208: Build context dictionary with all relevant info
        context = {
            "company_name": org_data.company_info.name,
            "industry": org_data.company_info.industry,
            "company_size": org_data.company_info.size,
            "location": org_data.company_info.location,
            "mission": org_data.culture.mission,
            "values": org_data.culture.values,
            "work_style": org_data.culture.work_style,
            "benefits": asdict(org_data.benefits),
            "salary_range": salary_range,
            "department_info": department_info,
            "tech_stack": org_data.tech_stack or [],
            "tools_platforms": org_data.tools_platforms or [],
            "certifications_preferred": org_data.certifications_preferred or []
        }
        
        return context
    except Exception as e:
        print(f"Error getting job context: {e}")
        return {}
```

**What this does:** Gathers all relevant company information for creating a job description - like collecting all the details about a company that would be useful for writing a job posting.

---

## 📁 **File 5: `job_description_agent.py`**
*The main AI brain that creates job descriptions*

### **Imports Section (Lines 1-9):**
```python
# Line 1: For accessing environment variables (like API keys)
import os                    
# Line 2: Type hints for better code documentation
from typing import Dict, Any, Optional  
# Line 3: Load secrets from .env file
from dotenv import load_dotenv          
# Line 4: AI prompt templates from LangChain
from langchain_core.prompts import PromptTemplate      
# Line 5: Parse AI output into structured format
from langchain_core.output_parsers import PydanticOutputParser  
# Line 6: Data validation and structure
from pydantic import BaseModel, Field  
# Line 7: Connect to OpenAI API
from openai import OpenAI              
# Line 8: Handle JSON data
import json                            
# Line 9: Import our company database
from knowledge_base import KnowledgeBase  
```

### **JobDescription Model (Lines 14-27):**
```python
class JobDescription(BaseModel):
    """Structured output for job description"""
    # Line 16: The official job title
    job_title: str = Field(description="The official job title")
    # Line 17: Which department this role belongs to
    department: str = Field(description="Department where the position belongs")
    # Line 18: Experience level needed (entry, mid, senior, etc.)
    experience_level: str = Field(description="Experience level required")
    # Line 19: Brief overview of what this job is about
    job_summary: str = Field(description="Brief overview of the role")
    # Line 20: List of main things this person will do
    key_responsibilities: list = Field(description="List of main job responsibilities")
    # Line 21: Required technical and soft skills
    required_skills: list = Field(description="List of required technical and soft skills")
    # Line 22: Nice-to-have skills (not required)
    preferred_skills: list = Field(description="List of preferred but not required skills")
    # Line 23: Education requirements
    education: str = Field(description="Educational requirements")
    # Line 24: Where the job is located (remote, office, hybrid)
    location: str = Field(description="Job location (remote, hybrid, on-site)")
    # Line 25: How much the job pays
    salary_range: str = Field(description="Expected salary range")
    # Line 26: What benefits are offered
    benefits: list = Field(description="List of benefits offered")
    # Line 27: Description of company culture
    company_culture: str = Field(description="Brief description of company culture and values")
```

**What this does:** Like a template form that ensures every job description has the same sections. This guarantees consistent output from the AI.

### **JobDescriptionAgent Class (Lines 29-321):**

#### **Initialization (Lines 30-65):**
```python
def __init__(self, model_name: str = "gpt-4o-mini", temperature: float = 0.7):
    """Initialize the job description agent"""
    # Line 32: Get the secret API key from environment
    api_key = os.getenv("OPENAI_API_KEY")
    # Line 33-34: Stop everything if no API key found
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not set")
    # Line 35: Create connection to OpenAI
    self.client = OpenAI(api_key=api_key)
    # Line 36: Remember which AI model to use
    self.model_name = model_name
    # Line 37: Remember creativity level (0=boring, 1=very creative)
    self.temperature = temperature

    # Line 39: Set up output parser (converts AI text to structured data)
    self.output_parser = PydanticOutputParser(pydantic_object=JobDescription)
    # Line 40: Connect to company database
    self.knowledge_base = KnowledgeBase()
    
    # Line 42-65: Create the AI prompt template
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
```

**What this does:** Sets up the AI agent like hiring an AI assistant and giving it:
1. Access to OpenAI (with your API key)
2. Instructions on which AI model to use
3. A creativity level setting
4. A detailed prompt template for generating job descriptions
5. Access to the company database

#### **Main Generation Method (Lines 67-105):**
```python
def generate_job_description(self, job_input: str, organization_id: Optional[str] = None):
    """Generate a job description from the input with optional organization context"""
    try:
        # Step 1: Get company information if provided
        organization_context = ""
        if organization_id:
            # Line 74-75: Figure out what role and experience level from input
            role, experience_level = self._extract_role_and_level(job_input)
            # Line 75: Get company-specific context
            context = self.knowledge_base.get_job_context(organization_id, role, experience_level)
            # Line 76: Format it nicely for the AI prompt
            organization_context = self._format_organization_context(context)
        
        # Step 2: Use default context if no company selected
        if not organization_context:
            organization_context = "Generate a general job description without specific company details."
        
        # Step 3: Build the complete prompt for AI
        prompt_text = self.prompt.format(
            job_input=job_input,
            organization_context=organization_context
        )
        
        # Step 4: Send request to OpenAI
        response = self.client.chat.completions.create(
            model=self.model_name,              # Which AI model to use
            temperature=self.temperature,       # Creativity level
            messages=[
                {"role": "system", "content": "You are a helpful assistant that returns only JSON."},
                {"role": "user", "content": prompt_text}
            ]
        )
        
        # Step 5: Extract the AI's response
        content = response.choices[0].message.content if response.choices else ""
        if not content:
            return None
        
        # Step 6: Convert AI response to structured JobDescription object
        return self.output_parser.parse(content)
        
    except Exception as e:
        print(f"Error generating job description: {e}")
        return None
```

**What this method does step-by-step:**
1. Gets company information if a company was selected
2. Creates a detailed prompt combining the user's input with company context
3. Sends the prompt to OpenAI's AI
4. Gets back the AI's response (should be structured JSON)
5. Converts the response into a JobDescription object
6. Returns the structured job description

#### **Helper Methods:**

**Extract Role and Experience (Lines 107-129):**
```python
def _extract_role_and_level(self, job_input: str) -> tuple[str, str]:
    """Extract role and experience level from job input"""
    # Line 109: Convert to lowercase for easier matching
    input_lower = job_input.lower()
    
    # Line 111-117: Define experience level keywords
    experience_keywords = {
        "entry": ["entry", "entry level", "junior", "fresh", "new graduate"],
        "mid": ["mid", "mid level", "intermediate", "experienced"],
        "senior": ["senior", "senior level", "lead", "principal"],
        "executive": ["executive", "director", "vp", "head", "chief"]
    }
    
    # Line 119-124: Find which experience level matches
    experience_level = "mid"  # default assumption
    for level, keywords in experience_keywords.items():
        if any(keyword in input_lower for keyword in keywords):
            experience_level = level
            break
    
    # Line 126-127: Extract role (simplified - just takes first word)
    role = job_input.split()[0] if job_input else "developer"
    
    return role, experience_level
```

**What this does:** Analyzes the user's input to figure out:
1. What type of role they want (developer, manager, etc.)
2. What experience level (entry, mid, senior, executive)

**Format Output (Lines 182-229):**
```python
def format_job_description(self, job_desc: JobDescription) -> str:
    """Format the job description for display"""
    if not job_desc:
        return "Error: Could not generate job description"
    
    # Build formatted string with markdown
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
    # Add numbered responsibilities
    for i, responsibility in enumerate(job_desc.key_responsibilities, 1):
        formatted += f"{i}. {responsibility}\n"
    
    # Add required skills as bullet points
    formatted += f"""
## Required Skills
"""
    for skill in job_desc.required_skills:
        formatted += f"• {skill}\n"
    
    # Add preferred skills if any exist
    if job_desc.preferred_skills:
        formatted += f"""
## Preferred Skills
"""
        for skill in job_desc.preferred_skills:
            formatted += f"• {skill}\n"
    
    # Add remaining sections
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
```

**What this does:** Takes the structured JobDescription object and converts it into a nicely formatted markdown document that looks professional.

---

## 📁 **File 6: `streamlit_app.py`**
*The web interface - what users see and interact with*

### **Imports Section (Lines 1-5):**
```python
# Line 1: Streamlit - framework for creating web apps in Python
import streamlit as st       
# Line 2: For accessing environment variables
import os                    
# Line 3: Load secret keys from .env file
from dotenv import load_dotenv  
# Line 4: Import our AI agent
from job_description_agent import JobDescriptionAgent  
# Line 5: For timing operations (used with loading spinners)
import time                  
```

### **Environment Setup (Lines 7-8):**
```python
# Line 7: Load environment variables from .env file
load_dotenv()
```

### **Page Configuration (Lines 10-15):**
```python
# Configure the web page settings
st.set_page_config(
    page_title="Job Description Agent",    # What shows in browser tab
    page_icon="🤖",                       # Icon in browser tab
    layout="wide"                         # Use full width of screen
)
```

### **CSS Styling (Lines 17-71):**
```python
# Custom CSS to make the page look beautiful
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;                 # Very large title text
        font-weight: bold;               # Make text bold
        text-align: center;              # Center the text
        margin-bottom: 2rem;             # Space below title
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);  # Gradient colors
        -webkit-background-clip: text;   # Apply gradient to text
        -webkit-text-fill-color: transparent;  # Make text transparent to show gradient
    }
    .sub-header {
        font-size: 1.2rem;              # Medium size text
        text-align: center;              # Center the text
        color: #666;                     # Gray color
        margin-bottom: 3rem;             # Space below
    }
    .input-container {
        background: #f8f9fa;            # Light gray background
        padding: 2rem;                  # Space inside container
        border-radius: 10px;            # Rounded corners
        border: 1px solid #e9ecef;      # Light border
        margin-bottom: 2rem;            # Space below container
    }
    .result-container {
        background: white;              # White background
        padding: 2rem;                  # Space inside
        border-radius: 10px;            # Rounded corners
        border: 1px solid #e9ecef;      # Light border
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);  # Drop shadow effect
    }
    .stButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);  # Gradient button
        color: white;                   # White text
        border: none;                   # No border
        padding: 0.75rem 2rem;          # Space inside button
        border-radius: 25px;            # Very rounded corners
        font-weight: bold;              # Bold text
        font-size: 1.1rem;              # Slightly larger text
    }
    .stButton > button:hover {
        background: linear-gradient(90deg, #5a6fd8 0%, #6a4190 100%);  # Darker on hover
        transform: translateY(-2px);    # Slight lift effect
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);  # Shadow when hovering
    }
    .example-text {
        background: #e3f2fd;           # Light blue background
        padding: 1rem;                 # Space inside
        border-radius: 8px;            # Rounded corners
        border-left: 4px solid #2196f3;  # Blue left border
        margin: 1rem 0;               # Space above and below
    }
</style>
""", unsafe_allow_html=True)
```

**What this does:** Makes the web page look professional and attractive by defining colors, fonts, spacing, and effects. Like interior decorating for a website.

### **Main Function (Lines 73-224):**

#### **Header Section (Lines 74-76):**
```python
def main():
    # Create the main title with custom styling
    st.markdown('<h1 class="main-header">🤖 Job Description Agent</h1>', unsafe_allow_html=True)
    # Create subtitle with description
    st.markdown('<p class="sub-header">Generate comprehensive job descriptions from simple inputs using AI</p>', unsafe_allow_html=True)
```

#### **Configuration Setup (Lines 78-81):**
```python
    # Get API key from environment variables
    api_key = os.getenv("OPENAI_API_KEY", "")
    # Set default AI model to use
    model_name = "gpt-4o-mini"  
    # Set default creativity level (0.7 = moderately creative)
    temperature = 0.7  
```

#### **Quick Examples Section (Lines 83-100):**
```python
    # Show section title
    st.markdown("### 📚 Quick Examples")
    st.markdown("Click any example to use it:")
    
    # Create 5 columns for example buttons
    col1, col2, col3, col4, col5 = st.columns(5)
    
    # List of example job descriptions
    examples = [
        "web developer with 5 years experience",
        "senior data scientist",
        "marketing manager entry level",
        "software engineer remote",
        "product manager fintech"
    ]
    
    # Create a button for each example
    for i, example in enumerate(examples):
        with [col1, col2, col3, col4, col5][i]:  # Use the i-th column
            if st.button(example, key=example, use_container_width=True):
                # If button clicked, set the input field to this example
                st.session_state.job_input = example
                st.rerun()  # Refresh the page to show the new input
```

**What this does:** Creates clickable example buttons that automatically fill in the input field when clicked.

#### **Main Content Layout (Lines 102-103):**
```python
    # Create two columns: main content (2/3 width) and sidebar (1/3 width)
    col1, col2 = st.columns([2, 1])
```

#### **Input Section (Lines 105-140):**
```python
    with col1:  # Left column - main input area
        st.markdown('<div class="input-container">', unsafe_allow_html=True)
        st.header("📝 Job Description Request")
        
        # Organization selection dropdown
        from knowledge_base import KnowledgeBase
        kb = KnowledgeBase()                    # Connect to company database
        organizations = kb.list_organizations() # Get list of available companies
        
        if organizations:                       # If companies exist
            st.subheader("🏢 Organization Selection")
            selected_org = st.selectbox(
                "Choose an organization (optional)",
                ["General Description"] + organizations,  # Add "General" option first
                help="Select an organization to generate company-specific job descriptions"
            )
            if selected_org == "General Description":
                selected_org = None             # No specific company selected
        else:
            selected_org = None
            st.info("💡 No organizations in knowledge base. Use the Knowledge Base Manager to add organizations.")
        
        # Main job input field
        job_input = st.text_input(
            "Describe the job position",
            placeholder="e.g., web developer with 5 years experience",
            key="job_input",                   # Links to session state for examples
            help="Enter a simple description of the job you want to create a description for"
        )
        
        # Generate button (centered)
        c1, c2, c3 = st.columns([1, 2, 1])    # Three columns to center the button
        with c2:                               # Use middle column
            generate_button = st.button("🚀 Generate Job Description", use_container_width=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
```

#### **Generation Logic (Lines 171-211):**
```python
    # Main generation process - runs when button is clicked and input exists
    if generate_button and job_input:
        # Check if API key exists
        if not api_key:
            st.error("❌ OpenAI API key not found. Please set the OPENAI_API_KEY environment variable or add it to your .env file.")
            st.info("💡 Create a .env file in the project root with: OPENAI_API_KEY=your_api_key_here")
            return
        
        try:
            # Show loading spinner while generating
            with st.spinner("🔄 Generating your job description..."):
                # Create AI agent
                agent = JobDescriptionAgent(model_name=model_name)
                agent.temperature = temperature
                
                # Generate the job description
                job_desc = agent.generate_job_description(job_input, selected_org)
                
                if job_desc:  # If generation successful
                    # Display results in styled container
                    st.markdown('<div class="result-container">', unsafe_allow_html=True)
                    st.success("✅ Job description generated successfully!")
                    
                    # Format and display the job description
                    formatted_output = agent.format_job_description(job_desc)
                    st.markdown(formatted_output)
                    
                    # Add download button
                    st.download_button(
                        label="📥 Download as Markdown",
                        data=formatted_output,
                        file_name=f"job_description_{job_desc.job_title.lower().replace(' ', '_')}.md",
                        mime="text/markdown"
                    )
                    
                    st.markdown("</div>", unsafe_allow_html=True)
                else:
                    st.error("❌ Failed to generate job description. Please try again.")
                    
        except Exception as e:
            st.error(f"❌ An error occurred: {str(e)}")
            st.info("Please check your API key and try again.")
```

**What this section does step-by-step:**
1. Checks if user clicked generate button AND entered input
2. Verifies API key exists
3. Shows loading spinner
4. Creates AI agent and generates job description
5. If successful: displays formatted result + download button
6. If failed: shows error message

---

## 📁 **File 7: `demo.py`**
*Example script showing how to use the agent*

### **File Header (Lines 1-5):**
```python
#!/usr/bin/env python3        # Tells system this is a Python script
"""
Demo script for the Job Description Agent
This script demonstrates the agent's capabilities with example inputs.
"""
```

### **Imports (Lines 7-8):**
```python
import os                     # For environment variables
from job_description_agent import JobDescriptionAgent  # Our AI agent
```

### **Main Demo Function (Lines 10-84):**
```python
def demo_job_description_agent():
    """Demonstrate the job description agent with example inputs"""
    
    # Check if API key exists
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ OPENAI_API_KEY not found in environment variables.")
        print("Please set your OpenAI API key before running the demo.")
        print("You can either:")
        print("1. Create a .env file with OPENAI_API_KEY=your_key")
        print("2. Set the environment variable: set OPENAI_API_KEY=your_key")
        return
    
    print("🤖 Job Description Agent Demo")
    print("=" * 50)
    
    # Create the AI agent
    agent = JobDescriptionAgent()
    
    # List of test examples
    examples = [
        "web developer with 5 years experience",
        "senior data scientist",
        "marketing manager entry level",
        "software engineer remote",
        "product manager fintech"
    ]
    
    print(f"Running {len(examples)} examples...\n")
    
    # Test each example
    for i, example in enumerate(examples, 1):
        print(f"📝 Example {i}: {example}")
        print("-" * 40)
        
        try:
            # Generate job description
            job_desc = agent.generate_job_description(example)
            
            if job_desc:  # If generation successful
                # Display basic information
                print(f"✅ Generated: {job_desc.job_title}")
                print(f"   Department: {job_desc.department}")
                print(f"   Experience: {job_desc.experience_level}")
                print(f"   Location: {job_desc.location}")
                print(f"   Salary: {job_desc.salary_range}")
                
                # Show first 100 characters of summary
                print(f"\n📋 Summary: {job_desc.job_summary[:100]}...")
                
                # Show first 3 required skills
                print(f"\n🔑 Key Skills: {', '.join(job_desc.required_skills[:3])}...")
                
                # Save to file
                filename = f"demo_job_{i}_{job_desc.job_title.lower().replace(' ', '_')}.md"
                formatted_output = agent.format_job_description(job_desc)
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(formatted_output)
                print(f"💾 Saved to: {filename}")
                
            else:
                print("❌ Failed to generate job description")
                
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print("\n" + "=" * 50 + "\n")
    
    # Final instructions
    print("🎉 Demo completed!")
    print("Check the generated .md files to see the full job descriptions.")
    print("\nTo run the full application:")
    print("• Web interface: streamlit run streamlit_app.py")
    print("• Command line: python job_description_agent.py")

# Run demo if script is executed directly
if __name__ == "__main__":
    demo_job_description_agent()
```

**What this script does:**
1. Checks if API key is set up
2. Creates an AI agent
3. Tests 5 different example job descriptions
4. For each example:
   - Generates a job description
   - Shows basic info (title, department, etc.)
   - Shows preview of summary and skills
   - Saves full result to a markdown file
5. Provides instructions for running the full application

---

## 📁 **File 8: `load_sample_data.py`**
*Loads example company data for testing*

### **File Header (Lines 1-5):**
```python
#!/usr/bin/env python3        # Python script indicator
"""
Sample Data Loader for HR Agent
Loads sample organizational data into the knowledge base.
"""
```

### **Imports (Lines 7-8):**
```python
import json                   # For handling JSON data
from knowledge_base import KnowledgeBase, OrganizationalData  # Our database system
```

### **Main Function (Lines 10-66):**
```python
def load_sample_data():
    """Load sample organizational data from sample_organizations.json"""
    
    print("🏢 Sample Data Loader")
    print("=" * 40)
    
    # Connect to the company database
    kb = KnowledgeBase()
    
    # Check if companies already exist
    existing_orgs = kb.list_organizations()
    if existing_orgs:
        print(f"Found {len(existing_orgs)} existing organizations:")
        for org in existing_orgs:
            print(f"  - {org}")
        
        # Ask user if they want to proceed
        choice = input("\nDo you want to load sample data anyway? (y/n): ").strip().lower()
        if choice not in ['y', 'yes']:
            print("❌ Sample data loading cancelled.")
            return
    
    print("📥 Loading sample organizations...")
    
    # The sample data is already in knowledge_base/organizations.json
    # This script just verifies it's loaded correctly
    organizations = kb.list_organizations()
    
    if not organizations:
        print("❌ No sample data found. Please check knowledge_base/organizations.json")
        return
    
    # Display information about each loaded organization
    success_count = 0
    for org_id in organizations:
        org_data = kb.get_organization(org_id)
        if org_data:
            print(f"Processing {org_id}...")
            print(f"✅ Successfully added {org_id}")
            success_count += 1
        else:
            print(f"❌ Failed to load {org_id}")
    
    print(f"\n🎉 Sample data loading completed!")
    print(f"\nAvailable organizations:")
    
    # Show details of loaded organizations
    for org_id in organizations:
        org_data = kb.get_organization(org_id)
        if org_data:
            print(f"  - {org_id}: {org_data.company_info.name}")
    
    print(f"\n💡 You can now use these organization IDs in the job description agent:")
    for org_id in organizations:
        print(f"   - {org_id}")

# Run if executed directly
if __name__ == "__main__":
    load_sample_data()
```

**What this script does:**
1. Connects to the company database
2. Checks if sample companies already exist
3. Asks user permission to proceed if data exists
4. Verifies that sample data is properly loaded
5. Shows success/failure for each company
6. Lists all available companies with their names
7. Tells user how to use the company IDs

---

## 📁 **Data Files Explained**

### **`knowledge_base/organizations.json`**
This JSON file contains detailed information about two example companies:

#### **TechCorp Solutions Structure:**
```json
{
  "techcorp": {                          // Company ID (used in code)
    "company_info": {                    // Basic company details
      "name": "TechCorp Solutions",      // Display name
      "industry": "Technology",          // What business they're in
      "size": "100-250 employees",       // Company size range
      "location": "San Francisco, CA",   // Where they're located
      "founded_year": 2018,              // When company started
      "website": "https://techcorp.com", // Company website
      "description": "Innovative technology company focused on AI and machine learning solutions."
    },
    "culture": {                         // Company personality
      "mission": "To democratize AI technology...",
      "vision": "To be the leading provider...",
      "values": ["Innovation", "Collaboration", "Excellence"],
      "work_style": "Collaborative and fast-paced",
      "diversity_inclusion": "Committed to building a diverse workplace",
      "work_life_balance": "Flexible work arrangements"
    },
    "benefits": {                        // What employees get
      "health_insurance": "Comprehensive health, dental, and vision coverage",
      "retirement_plans": "401(k) with company match up to 6%",
      "paid_time_off": "Unlimited PTO with 15 paid holidays",
      "flexible_work": "Hybrid work model with remote options",
      "professional_development": "Annual learning budget",
      "additional_benefits": ["Stock options", "Free lunch", "Gym membership"]
    },
    "salary_ranges": {                   // Pay scales by experience level
      "entry_level": {                   // New graduate level
        "software engineer": "$80,000 - $100,000",
        "data scientist": "$85,000 - $110,000"
      },
      "mid_level": {                     // 2-5 years experience
        "software engineer": "$110,000 - $140,000"
      },
      "senior_level": {                  // 5+ years experience
        "software engineer": "$140,000 - $180,000"
      },
      "executive_level": {               // Leadership positions
        "engineering manager": "$180,000 - $250,000"
      }
    },
    "departments": [                     // Different teams in company
      {
        "name": "Engineering",
        "description": "Core development team building AI-powered products",
        "typical_roles": ["Software Engineer", "DevOps Engineer"],
        "growth_opportunities": "Technical leadership, architecture roles",
        "team_size": "50-75 engineers"
      }
    ],
    "tech_stack": ["Python", "JavaScript", "React", "TensorFlow", "AWS"],
    "tools_platforms": ["GitHub", "Jira", "Slack", "Notion"],
    "certifications_preferred": ["AWS Certified", "Google Cloud Professional"],
    "last_updated": "2024-08-20T18:21:00"
  }
}
```

### **`knowledge_base/job_templates.json`**
Templates for different company types:

```json
{
  "tech_company": {                      // Template for technology companies
    "culture_keywords": [                // Words that describe tech company culture
      "innovative", "fast-paced", "collaborative", "growth-oriented"
    ],
    "benefits_emphasis": [               // Benefits to highlight for tech companies
      "flexible work", "professional development", "health benefits"
    ],
    "tech_focus": true                   // This type emphasizes technical skills
  },
  "startup": {                           // Template for startup companies
    "culture_keywords": [
      "dynamic", "entrepreneurial", "flexible", "impact-driven"
    ],
    "benefits_emphasis": [
      "equity", "flexible hours", "remote work"
    ],
    "tech_focus": true
  },
  "enterprise": {                        // Template for large corporations
    "culture_keywords": [
      "stable", "professional", "structured", "career growth"
    ],
    "benefits_emphasis": [
      "comprehensive benefits", "retirement plans", "professional development"
    ],
    "tech_focus": false                  // Less emphasis on technical skills
  },
  "non_profit": {                        // Template for non-profit organizations
    "culture_keywords": [
      "mission-driven", "collaborative", "meaningful work", "community-focused"
    ],
    "benefits_emphasis": [
      "work-life balance", "meaningful impact", "flexible arrangements"
    ],
    "tech_focus": false
  }
}
```

---

## 🔄 **How Everything Works Together**

### **The Complete Flow:**

1. **User starts the application**
   - Runs `start.bat` or `streamlit run streamlit_app.py`
   - Web interface loads (`streamlit_app.py`)

2. **User interacts with the interface**
   - Selects a company (optional) from dropdown
   - Types job description (e.g., "senior web developer")
   - Clicks "Generate" button

3. **System processes the request**
   - `streamlit_app.py` calls `JobDescriptionAgent.generate_job_description()`
   - Agent extracts role and experience level from input
   - If company selected, agent gets company context from `KnowledgeBase`

4. **AI generation happens**
   - Agent builds detailed prompt combining user input + company context
   - Sends prompt to OpenAI GPT model
   - Receives structured JSON response

5. **Result processing**
   - AI response converted to `JobDescription` object
   - Object formatted into readable markdown
   - Result displayed in web interface
   - User can download as file

### **Key Design Principles:**

1. **Separation of Concerns:**
   - `streamlit_app.py` - User interface only
   - `job_description_agent.py` - AI logic only  
   - `knowledge_base.py` - Data management only

2. **Structured Data:**
   - Pydantic models ensure consistent output format
   - JSON files for easy data storage and editing
   - Type hints throughout for better code reliability

3. **Error Handling:**
   - API key validation
   - Graceful failure with user-friendly messages
   - Try/catch blocks around risky operations

4. **User Experience:**
   - Loading spinners during AI generation
   - Example buttons for quick testing
   - Download functionality for results
   - Clean, professional interface design

5. **Extensibility:**
   - Easy to add new company types
   - Simple to modify prompt templates
   - Modular design allows feature additions

---

## 🎯 **For Prompt Engineers**

### **Key Concepts to Understand:**

1. **Prompt Engineering in Practice:**
   - Look at lines 43-65 in `job_description_agent.py`
   - This shows how to structure prompts for consistent AI output
   - Notice how company context is injected into the prompt

2. **Structured Output:**
   - The `JobDescription` class (lines 14-27) defines the exact structure
   - Pydantic ensures AI output matches this structure
   - This is crucial for reliable AI applications

3. **Context Management:**
   - `get_job_context()` method shows how to gather relevant information
   - Company data enriches the AI prompt with specific details
   - This makes outputs more realistic and tailored

4. **Error Handling:**
   - Multiple fallback strategies when things go wrong
   - User-friendly error messages instead of technical crashes
   - Graceful degradation (works without company data)

5. **Data Flow:**
   - Simple user input → Enhanced prompt → AI generation → Structured output
   - Each step is modular and testable
   - Easy to debug when issues occur

This codebase demonstrates professional AI application development with proper prompt engineering, structured outputs, and user experience considerations.
