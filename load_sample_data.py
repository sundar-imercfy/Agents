#!/usr/bin/env python3
"""
Sample Data Loader for HR Agent
Loads sample organizational data into the knowledge base.
"""

import json
from knowledge_base import KnowledgeBase, OrganizationalData

def load_sample_data():
    """Load sample organizational data from sample_organizations.json"""
    
    print("🏢 Sample Data Loader")
    print("=" * 40)
    
    # Initialize knowledge base
    kb = KnowledgeBase()
    
    # Check existing organizations
    existing_orgs = kb.list_organizations()
    if existing_orgs:
        print(f"Found {len(existing_orgs)} existing organizations:")
        for org in existing_orgs:
            print(f"  - {org}")
        
        choice = input("\nDo you want to load sample data anyway? (y/n): ").strip().lower()
        if choice not in ['y', 'yes']:
            print("❌ Sample data loading cancelled.")
            return
    
    print("📥 Loading sample organizations...")
    
    # Sample data is already in the knowledge_base/organizations.json file
    # We just need to confirm it's loaded properly
    organizations = kb.list_organizations()
    
    if not organizations:
        print("❌ No sample data found. Please check knowledge_base/organizations.json")
        return
    
    # Display loaded organizations
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
    
    for org_id in organizations:
        org_data = kb.get_organization(org_id)
        if org_data:
            print(f"  - {org_id}: {org_data.company_info.name}")
    
    print(f"\n💡 You can now use these organization IDs in the job description agent:")
    for org_id in organizations:
        print(f"   - {org_id}")

if __name__ == "__main__":
    load_sample_data()
