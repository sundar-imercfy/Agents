import json
import os
from typing import Dict, List, Optional, Any
from datetime import datetime
from dataclasses import dataclass, asdict
from pathlib import Path

@dataclass
class CompanyInfo:
    """Company basic information"""
    name: str
    industry: str
    size: str  # e.g., "50-100 employees", "500+ employees"
    location: str
    founded_year: Optional[int] = None
    website: Optional[str] = None
    description: Optional[str] = None

@dataclass
class CompanyCulture:
    """Company culture and values"""
    mission: str
    vision: str
    values: List[str]
    work_style: str  # e.g., "collaborative", "autonomous", "fast-paced"
    diversity_inclusion: str
    work_life_balance: str

@dataclass
class BenefitsPackage:
    """Company benefits and perks"""
    health_insurance: str
    retirement_plans: str
    paid_time_off: str
    flexible_work: str  # remote, hybrid, on-site options
    professional_development: str
    additional_benefits: List[str]

@dataclass
class SalaryRanges:
    """Salary ranges by role and experience level"""
    entry_level: Dict[str, str]  # role: salary_range
    mid_level: Dict[str, str]
    senior_level: Dict[str, str]
    executive_level: Dict[str, str]

@dataclass
class DepartmentInfo:
    """Department-specific information"""
    name: str
    description: str
    typical_roles: List[str]
    growth_opportunities: str
    team_size: str

@dataclass
class OrganizationalData:
    """Complete organizational data structure"""
    company_info: CompanyInfo
    culture: CompanyCulture
    benefits: BenefitsPackage
    salary_ranges: SalaryRanges
    departments: List[DepartmentInfo]
    tech_stack: List[str] = None
    tools_platforms: List[str] = None
    certifications_preferred: List[str] = None
    last_updated: str = None

class KnowledgeBase:
    """Knowledge base for storing and managing organizational data"""
    
    def __init__(self, data_dir: str = "knowledge_base"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        self.organizations_file = self.data_dir / "organizations.json"
        self.templates_file = self.data_dir / "job_templates.json"
        
        # Initialize files if they don't exist
        self._initialize_files()
    
    def _initialize_files(self):
        """Initialize knowledge base files if they don't exist"""
        if not self.organizations_file.exists():
            self._save_organizations({})
        
        if not self.templates_file.exists():
            self._save_templates(self._get_default_templates())
    
    def _get_default_templates(self) -> Dict[str, Any]:
        """Get default job description templates"""
        return {
            "tech_company": {
                "culture_keywords": ["innovative", "fast-paced", "collaborative", "growth-oriented"],
                "benefits_emphasis": ["flexible work", "professional development", "health benefits"],
                "tech_focus": True
            },
            "startup": {
                "culture_keywords": ["dynamic", "entrepreneurial", "flexible", "impact-driven"],
                "benefits_emphasis": ["equity", "flexible hours", "remote work"],
                "tech_focus": True
            },
            "enterprise": {
                "culture_keywords": ["stable", "professional", "structured", "career growth"],
                "benefits_emphasis": ["comprehensive benefits", "retirement plans", "professional development"],
                "tech_focus": False
            },
            "non_profit": {
                "culture_keywords": ["mission-driven", "collaborative", "meaningful work", "community-focused"],
                "benefits_emphasis": ["work-life balance", "meaningful impact", "flexible arrangements"],
                "tech_focus": False
            }
        }
    
    def add_organization(self, org_id: str, data: OrganizationalData) -> bool:
        """Add or update an organization in the knowledge base"""
        try:
            organizations = self._load_organizations()
            
            # Update last_updated timestamp
            data.last_updated = datetime.now().isoformat()
            
            # Convert to dictionary
            org_data = asdict(data)
            organizations[org_id] = org_data
            
            self._save_organizations(organizations)
            return True
        except Exception as e:
            print(f"Error adding organization: {e}")
            return False
    
    def get_organization(self, org_id: str) -> Optional[OrganizationalData]:
        """Retrieve organization data by ID"""
        try:
            organizations = self._load_organizations()
            if org_id in organizations:
                org_data = organizations[org_id]
                return self._dict_to_organizational_data(org_data)
            return None
        except Exception as e:
            print(f"Error retrieving organization: {e}")
            return None
    
    def list_organizations(self) -> List[str]:
        """List all organization IDs in the knowledge base"""
        try:
            organizations = self._load_organizations()
            return list(organizations.keys())
        except Exception as e:
            print(f"Error listing organizations: {e}")
            return []
    
    def delete_organization(self, org_id: str) -> bool:
        """Delete an organization from the knowledge base"""
        try:
            organizations = self._load_organizations()
            if org_id in organizations:
                del organizations[org_id]
                self._save_organizations(organizations)
                return True
            return False
        except Exception as e:
            print(f"Error deleting organization: {e}")
            return False
    
    def update_organization_field(self, org_id: str, field: str, value: Any) -> bool:
        """Update a specific field in an organization's data"""
        try:
            organizations = self._load_organizations()
            if org_id in organizations:
                org_data = organizations[org_id]
                org_data[field] = value
                org_data['last_updated'] = datetime.now().isoformat()
                self._save_organizations(organizations)
                return True
            return False
        except Exception as e:
            print(f"Error updating organization field: {e}")
            return False
    
    def get_job_context(self, org_id: str, role: str, experience_level: str) -> Dict[str, Any]:
        """Get contextual information for job description generation"""
        try:
            org_data = self.get_organization(org_id)
            if not org_data:
                return {}
            
            # Get salary range for the role and experience level
            salary_range = self._get_salary_range(org_data.salary_ranges, role, experience_level)
            
            # Get department info if available
            department_info = self._get_department_info(org_data.departments, role)
            
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
    
    def _get_salary_range(self, salary_ranges: SalaryRanges, role: str, experience_level: str) -> str:
        """Get salary range for a specific role and experience level"""
        level_map = {
            "entry": salary_ranges.entry_level,
            "junior": salary_ranges.entry_level,
            "mid": salary_ranges.mid_level,
            "senior": salary_ranges.senior_level,
            "executive": salary_ranges.executive_level
        }
        
        level_data = level_map.get(experience_level.lower(), salary_ranges.mid_level)
        return level_data.get(role.lower(), "Competitive salary based on experience")
    
    def _get_department_info(self, departments: List[DepartmentInfo], role: str) -> Optional[Dict[str, Any]]:
        """Get department information for a specific role"""
        for dept in departments:
            if role.lower() in [r.lower() for r in dept.typical_roles]:
                return asdict(dept)
        return None
    
    def _load_organizations(self) -> Dict[str, Any]:
        """Load organizations data from file"""
        try:
            with open(self.organizations_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
        except Exception as e:
            print(f"Error loading organizations: {e}")
            return {}
    
    def _save_organizations(self, organizations: Dict[str, Any]):
        """Save organizations data to file"""
        try:
            with open(self.organizations_file, 'w', encoding='utf-8') as f:
                json.dump(organizations, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving organizations: {e}")
    
    def _load_templates(self) -> Dict[str, Any]:
        """Load job templates from file"""
        try:
            with open(self.templates_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return self._get_default_templates()
        except Exception as e:
            print(f"Error loading templates: {e}")
            return self._get_default_templates()
    
    def _save_templates(self, templates: Dict[str, Any]):
        """Save job templates to file"""
        try:
            with open(self.templates_file, 'w', encoding='utf-8') as f:
                json.dump(templates, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving templates: {e}")
    
    def _dict_to_organizational_data(self, data: Dict[str, Any]) -> OrganizationalData:
        """Convert dictionary back to OrganizationalData object"""
        return OrganizationalData(
            company_info=CompanyInfo(**data['company_info']),
            culture=CompanyCulture(**data['culture']),
            benefits=BenefitsPackage(**data['benefits']),
            salary_ranges=SalaryRanges(**data['salary_ranges']),
            departments=[DepartmentInfo(**dept) for dept in data['departments']],
            tech_stack=data.get('tech_stack'),
            tools_platforms=data.get('tools_platforms'),
            certifications_preferred=data.get('certifications_preferred'),
            last_updated=data.get('last_updated')
        )
    
    def export_organization(self, org_id: str, filepath: str) -> bool:
        """Export organization data to a JSON file"""
        try:
            org_data = self.get_organization(org_id)
            if org_data:
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(asdict(org_data), f, indent=2, ensure_ascii=False)
                return True
            return False
        except Exception as e:
            print(f"Error exporting organization: {e}")
            return False
    
    def import_organization(self, org_id: str, filepath: str) -> bool:
        """Import organization data from a JSON file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            org_data = self._dict_to_organizational_data(data)
            return self.add_organization(org_id, org_data)
        except Exception as e:
            print(f"Error importing organization: {e}")
            return False
