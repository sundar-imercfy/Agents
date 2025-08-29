#!/usr/bin/env python3
"""
Demo script for the HR Job Description Generator
This script demonstrates the agent's capabilities with example inputs.
"""

import os
from job_description_agent import JobDescriptionAgent

def demo_job_description_agent():
    """Demonstrate the job description agent with example inputs"""
    
    # Check if API key is set
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ OPENAI_API_KEY not found in environment variables.")
        print("Please set your OpenAI API key before running the demo.")
        print("You can either:")
        print("1. Create a .env file with OPENAI_API_KEY=your_key")
        print("2. Set the environment variable: set OPENAI_API_KEY=your_key")
        return
    
    print("🤖 HR Job Description Generator Demo")
    print("=" * 50)
    
    # Initialize the agent
    agent = JobDescriptionAgent()
    
    # Example inputs to demonstrate
    examples = [
        "web developer with 5 years experience",
        "senior data scientist",
        "marketing manager entry level",
        "software engineer remote",
        "product manager fintech"
    ]
    
    print(f"Running {len(examples)} examples...\n")
    
    for i, example in enumerate(examples, 1):
        print(f"📝 Example {i}: {example}")
        print("-" * 40)
        
        try:
            # Generate job description
            job_desc = agent.generate_job_description(example)
            
            if job_desc:
                # Display basic info
                print(f"✅ Generated: {job_desc.job_title}")
                print(f"   Department: {job_desc.department}")
                print(f"   Experience: {job_desc.experience_level}")
                print(f"   Location: {job_desc.location}")
                print(f"   Salary: {job_desc.salary_range}")
                
                # Show summary
                print(f"\n📋 Summary: {job_desc.job_summary[:100]}...")
                
                # Show key skills
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
    
    print("🎉 Demo completed!")
    print("Check the generated .md files to see the full job descriptions.")
    print("\nTo run the full application:")
    print("• Web interface: streamlit run streamlit_app.py")
    print("• Command line: python job_description_agent.py")

if __name__ == "__main__":
    demo_job_description_agent()