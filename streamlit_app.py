import streamlit as st
import os
from dotenv import load_dotenv
from job_description_agent import JobDescriptionAgent
import time

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
	page_title="Job Description Agent",
	page_icon="🤖",
	layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
	.main-header {
		font-size: 3rem;
		font-weight: bold;
		text-align: center;
		margin-bottom: 2rem;
		background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
		-webkit-background-clip: text;
		-webkit-text-fill-color: transparent;
	}
	.sub-header {
		font-size: 1.2rem;
		text-align: center;
		color: #666;
		margin-bottom: 3rem;
	}
	.input-container {
		background: #f8f9fa;
		padding: 2rem;
		border-radius: 10px;
		border: 1px solid #e9ecef;
		margin-bottom: 2rem;
	}
	.result-container {
		background: white;
		padding: 2rem;
		border-radius: 10px;
		border: 1px solid #e9ecef;
		box-shadow: 0 2px 10px rgba(0,0,0,0.1);
	}
	.stButton > button {
		background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
		color: white;
		border: none;
		padding: 0.75rem 2rem;
		border-radius: 25px;
		font-weight: bold;
		font-size: 1.1rem;
	}
	.stButton > button:hover {
		background: linear-gradient(90deg, #5a6fd8 0%, #6a4190 100%);
		transform: translateY(-2px);
		box-shadow: 0 4px 15px rgba(0,0,0,0.2);
	}
	.example-text {
		background: #e3f2fd;
		padding: 1rem;
		border-radius: 8px;
		border-left: 4px solid #2196f3;
		margin: 1rem 0;
	}
</style>
""", unsafe_allow_html=True)

def main():
	# Header
	st.markdown('<h1 class="main-header">🤖 Job Description Agent</h1>', unsafe_allow_html=True)
	st.markdown('<p class="sub-header">Generate comprehensive job descriptions from simple inputs using AI</p>', unsafe_allow_html=True)
	
	# Set default configuration values
	api_key = os.getenv("OPENAI_API_KEY", "")
	model_name = "gpt-4o-mini"  # Default model
	temperature = 0.7  # Default creativity level
	
	# Quick examples section
	st.markdown("### 📚 Quick Examples")
	st.markdown("Click any example to use it:")
	
	col1, col2, col3, col4, col5 = st.columns(5)
	examples = [
		"web developer with 5 years experience",
		"senior data scientist",
		"marketing manager entry level",
		"software engineer remote",
		"product manager fintech"
	]
	
	for i, example in enumerate(examples):
		with [col1, col2, col3, col4, col5][i]:
			if st.button(example, key=example, use_container_width=True):
				st.session_state.job_input = example
				st.rerun()
	
	# Main content
	col1, col2 = st.columns([2, 1])
	
	with col1:
		st.markdown('<div class="input-container">', unsafe_allow_html=True)
		st.header("📝 Job Description Request")
		
		# Organization selection
		from knowledge_base import KnowledgeBase
		kb = KnowledgeBase()
		organizations = kb.list_organizations()
		
		if organizations:
			st.subheader("🏢 Organization Selection")
			selected_org = st.selectbox(
				"Choose an organization (optional)",
				["General Description"] + organizations,
				help="Select an organization to generate company-specific job descriptions"
			)
			if selected_org == "General Description":
				selected_org = None
		else:
			selected_org = None
			st.info("💡 No organizations in knowledge base. Use the Knowledge Base Manager to add organizations.")
		
		# Job input
		job_input = st.text_input(
			"Describe the job position",
			placeholder="e.g., web developer with 5 years experience",
			key="job_input",
			help="Enter a simple description of the job you want to create a description for"
		)
		
		# Generate button
		c1, c2, c3 = st.columns([1, 2, 1])
		with c2:
			generate_button = st.button("🚀 Generate Job Description", use_container_width=True)
		
		st.markdown("</div>", unsafe_allow_html=True)
		
		# Examples
		st.markdown('<div class="example-text">', unsafe_allow_html=True)
		st.markdown("**💡 Examples:**")
		st.markdown("- `senior python developer`")
		st.markdown("- `marketing coordinator entry level`")
		st.markdown("- `data analyst with 3 years experience`")
		st.markdown("- `product manager remote`")
		st.markdown("</div>", unsafe_allow_html=True)
	
	with col2:
		st.markdown('<div class="input-container">', unsafe_allow_html=True)
		st.header("📊 Features")
		
		features = [
			"✅ Professional formatting",
			"✅ Industry-standard sections",
			"✅ Inclusive language",
			"✅ Realistic requirements",
			"✅ Salary expectations",
			"✅ Company culture",
			"✅ Benefits package",
			"✅ Export to Markdown"
		]
		
		for feature in features:
			st.markdown(feature)
		
		st.markdown("</div>", unsafe_allow_html=True)
	
	# Generate job description
	if generate_button and job_input:
		if not api_key:
			st.error("❌ OpenAI API key not found. Please set the OPENAI_API_KEY environment variable or add it to your .env file.")
			st.info("💡 Create a .env file in the project root with: OPENAI_API_KEY=your_api_key_here")
			return
		
		try:
			with st.spinner("🔄 Generating your job description..."):
				# Initialize agent
				agent = JobDescriptionAgent(model_name=model_name)
				agent.temperature = temperature
				
				# Generate description
				job_desc = agent.generate_job_description(job_input, selected_org)
				
				if job_desc:
					# Display results
					st.markdown('<div class="result-container">', unsafe_allow_html=True)
					st.success("✅ Job description generated successfully!")
					
					# Format and display
					formatted_output = agent.format_job_description(job_desc)
					st.markdown(formatted_output)
					
					# Download button
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
	
	# Footer
	st.markdown("---")
	st.markdown(
		"<div style='text-align: center; color: #666;'>"
		"Built with ❤️ using LangChain and Streamlit | "
		"Powered by OpenAI GPT models"
		"</div>",
		unsafe_allow_html=True
	)

if __name__ == "__main__":
	main()
