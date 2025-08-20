# 🤖 Job Description Agent

An intelligent AI-powered tool that generates comprehensive, professional job descriptions from simple inputs using LangChain and OpenAI's GPT models.

## ✨ Features

- **Simple Input**: Generate detailed job descriptions from basic descriptions like "web developer with 5 years experience"
- **Professional Output**: Industry-standard job description format with all essential sections
- **AI-Powered**: Uses OpenAI's GPT models for intelligent, context-aware content generation
- **Knowledge Base Integration**: Company-specific job descriptions using organizational data
- **Structured Output**: Consistent formatting with Pydantic models for reliable results
- **Multiple Interfaces**: Command-line tool and modern Streamlit web interface
- **Export Options**: Save job descriptions as Markdown files
- **Customizable**: Adjust creativity levels and choose different AI models
- **Organization Management**: Add, edit, and manage company data through interactive tools

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

### Installation

1. **Clone or download this repository**
   ```bash
   git clone <repository-url>
   cd "HR agent"
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your OpenAI API key**
   
   **Option A: Environment file (recommended)**
   ```bash
   # Copy the example file
   copy env_example.txt .env
   
   # Edit .env and add your API key
   OPENAI_API_KEY=your_actual_api_key_here
   ```
   
   **Option B: Set environment variable**
   ```bash
   # Windows
   set OPENAI_API_KEY=your_actual_api_key_here
   
   # macOS/Linux
   export OPENAI_API_KEY=your_actual_api_key_here
   ```

## 🎯 Usage

### Knowledge Base Setup (Optional but Recommended)

First, set up your organizational data for company-specific job descriptions:

```bash
# Load sample organizations for testing
python load_sample_data.py

# Or manage organizations interactively
python knowledge_base_manager.py
```

### Web Interface (Recommended)

Launch the Streamlit web app for a user-friendly experience:

```bash
streamlit run streamlit_app.py
```

The web interface will open in your browser with:
- Clean, modern design
- Easy input forms
- Organization selection dropdown
- Real-time generation
- Download options
- Configuration settings

### Command Line Interface

For terminal-based usage:

```bash
python job_description_agent.py
```

Follow the prompts to enter job descriptions and select organizations.

## 📝 Example Inputs

The agent works with various input formats:

- **Simple roles**: `web developer`, `data scientist`, `marketing manager`
- **With experience**: `senior developer with 5 years experience`
- **Entry level**: `junior analyst entry level`
- **Remote work**: `software engineer remote`
- **Industry specific**: `product manager fintech`
- **Combined**: `senior python developer with 3 years experience remote`

## 🏗️ Architecture

### Core Components

- **JobDescriptionAgent**: Main agent class using LangChain
- **JobDescription**: Pydantic model for structured output
- **KnowledgeBase**: Organizational data management system
- **Prompt Templates**: Professional HR-focused prompts with company context
- **Output Parsing**: Structured parsing with Pydantic
- **Formatting**: Clean Markdown output generation

### Technology Stack

- **LangChain**: AI application framework
- **OpenAI GPT**: Large language models
- **Pydantic**: Data validation and serialization
- **Streamlit**: Web interface framework
- **Python-dotenv**: Environment variable management
- **JSON**: Data persistence for organizational information

## 🔧 Configuration

### Model Selection

Choose from available OpenAI models:
- `gpt-3.5-turbo` (default, cost-effective)
- `gpt-4` (higher quality, more expensive)
- `gpt-4-turbo-preview` (latest features)

### Temperature Control

Adjust creativity levels:
- **Low (0.0-0.3)**: Consistent, focused output
- **Medium (0.4-0.7)**: Balanced creativity (default)
- **High (0.8-1.0)**: More creative, varied output

## 📊 Output Structure

Generated job descriptions include:

1. **Job Title & Basic Info**
   - Department, experience level, location, salary range

2. **Job Summary**
   - Concise overview of the role

3. **Key Responsibilities**
   - Numbered list of main duties

4. **Required Skills**
   - Technical and soft skills needed

5. **Preferred Skills**
   - Bonus qualifications

6. **Education Requirements**
   - Academic background needed

7. **Benefits Package**
   - Compensation and perks

8. **Company Culture**
   - Values and work environment

## 💡 Best Practices

### Input Tips
- Be specific about experience level
- Mention industry if relevant
- Include location preferences
- Specify remote/hybrid/on-site

### Output Usage
- Review and customize generated content
- Adjust requirements to match your company
- Add company-specific details
- Ensure compliance with local labor laws

## 🛠️ Development

### Project Structure
```
HR agent/
├── job_description_agent.py    # Core agent logic
├── knowledge_base.py          # Knowledge base system
├── knowledge_base_manager.py  # Interactive KB manager
├── streamlit_app.py           # Web interface
├── load_sample_data.py        # Sample data loader
├── sample_organizations.json  # Sample organization data
├── requirements.txt           # Dependencies
├── env_example.txt           # Environment template
└── README.md                 # This file
```

### Adding Custom Features

1. **Extend JobDescription Model**: Add new fields to the Pydantic model
2. **Custom Prompts**: Modify prompt templates for specific industries
3. **Additional Output Formats**: Create new formatters (PDF, Word, etc.)
4. **Integration**: Connect with HR systems or job boards

## 🔒 Security & Privacy

- API keys are stored locally in environment variables
- No job descriptions are stored on external servers
- Generated content is processed locally
- Follow OpenAI's data usage policies

## 📈 Performance Tips

- Use `gpt-3.5-turbo` for cost-effective generation
- Lower temperature for consistent results
- Batch multiple job descriptions if needed
- Cache common job types for reuse

## 🆘 Troubleshooting

### Common Issues

**API Key Errors**
- Verify your OpenAI API key is correct
- Check account has sufficient credits
- Ensure environment variable is set properly

**Generation Failures**
- Try different input phrasing
- Adjust temperature settings
- Check API rate limits

**Installation Issues**
- Update Python to 3.8+
- Use virtual environment
- Check pip version compatibility

### Getting Help

1. Check OpenAI API status
2. Verify your API key permissions
3. Review error messages for specific issues
4. Try simpler input formats

## 🤝 Contributing

Contributions are welcome! Areas for improvement:
- Additional output formats
- Industry-specific templates
- Multi-language support
- Integration with HR platforms
- Enhanced UI/UX features

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- Built with [LangChain](https://langchain.com/)
- Powered by [OpenAI](https://openai.com/) GPT models
- UI framework by [Streamlit](https://streamlit.io/)
- Data validation with [Pydantic](https://pydantic-docs.helpmanual.io/)

---

**Happy job description writing! 🎉**
