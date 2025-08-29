#!/usr/bin/env python3
"""
Streamlit Web Interface for Job Description Agent
Clean, minimal interface with no configuration options
"""

import streamlit as st
import os
from dotenv import load_dotenv
from job_description_agent import JobDescriptionAgent

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="HR Job Description Generator",
    page_icon="🤖",
    layout="wide"
)

def main():
    """Main Streamlit application"""
    
    # Header
    st.title("🤖 HR Job Description Generator")
    st.markdown("**Generate professional job descriptions instantly using AI**")
    st.markdown("---")
    
    # Check API key
    api_key = os.getenv("OPENAI_API_KEY", "")
    if not api_key:
        st.error("❌ OpenAI API key not found. Please check your .env file.")
        return
    
    # Sidebar with examples
    with st.sidebar:
        st.header("📚 Quick Examples")
        st.markdown("Click any example to try it:")
        
        examples = [
            "senior python developer",
            "marketing manager entry level", 
            "data analyst with 3 years experience",
            "software engineer remote",
            "product manager fintech"
        ]
        
        for example in examples:
            if st.button(example, key=f"ex_{example}", use_container_width=True):
                st.session_state['job_input'] = example
                st.rerun()
    
    # Main input area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Job description input
        job_input = st.text_area(
            "**Describe the job position:**",
            value=st.session_state.get('job_input', ''),
            height=120,
            placeholder="e.g., senior software engineer with 5 years experience in Python",
            help="Enter a simple description of the job role you want to create"
        )
        
        # Generate button
        if st.button("🚀 Generate Job Description", type="primary", use_container_width=True):
            if job_input.strip():
                with st.spinner("🔄 Generating professional job description..."):
                    try:
                        # Initialize agent with default settings
                        agent = JobDescriptionAgent(model_name="gpt-4o-mini")
                        
                        # Generate job description
                        job_desc = agent.generate_job_description(job_input)
                        
                        if job_desc:
                            # Format output
                            formatted_output = agent.format_job_description(job_desc)
                            
                            # Success message
                            st.success("✅ Job description generated successfully!")
                            
                            # Display result
                            st.markdown("### 📄 Generated Job Description")
                            st.markdown(formatted_output)
                            
                            # Download button
                            st.download_button(
                                label="📥 Download as Markdown File",
                                data=formatted_output,
                                file_name=f"job_description_{job_desc.job_title.lower().replace(' ', '_')}.md",
                                mime="text/markdown",
                                use_container_width=True
                            )
                            
                            # Celebration
                            st.balloons()
                            
                        else:
                            st.error("❌ Failed to generate job description. Please try again with different input.")
                            
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
                        st.info("💡 Try rephrasing your input or check your API configuration.")
            else:
                st.warning("⚠️ Please enter a job description to generate.")
    
    with col2:
        # Features list
        st.markdown("### ✨ Features")
        features = [
            "🎯 Professional formatting",
            "📋 Industry-standard sections",
            "🌍 Inclusive language", 
            "💰 Realistic salary ranges",
            "🏢 Company culture info",
            "🎁 Benefits package",
            "📄 Markdown export",
            "⚡ Instant generation"
        ]
        
        for feature in features:
            st.markdown(feature)
        
        # Info box
        st.info("💡 **Tip:** Be specific about experience level, skills, and work arrangement (remote/on-site) for best results.")

if __name__ == "__main__":
    main()

