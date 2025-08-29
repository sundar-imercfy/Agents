# 🤖 HR Job Description Generator

A simple, powerful AI tool that generates professional job descriptions from basic inputs using OpenAI's GPT models.

## ✨ Features

- **Simple Input**: Generate detailed job descriptions from basic descriptions
- **Professional Output**: Industry-standard job description format
- **AI-Powered**: Uses OpenAI GPT models for intelligent content generation
- **Clean Interface**: Modern Streamlit web interface
- **Export Options**: Download job descriptions as Markdown files
- **No Configuration**: Works out of the box with minimal setup

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
   
   Copy the example file and add your API key:
   ```bash
   copy env_example.txt .env
   ```
   
   Edit `.env` and add your API key:
   ```
   OPENAI_API_KEY=your_actual_api_key_here
   ```

## 🎯 Usage

### Web Interface (Recommended)

Launch the Streamlit web app:

```bash
streamlit run streamlit_app.py
```

The web interface provides:
- Clean, modern design
- Easy input forms
- Clickable examples
- Real-time generation
- Download options

### Command Line Interface

For terminal-based usage:

```bash
python job_description_agent.py
```

## 📝 Example Inputs

The agent works with various input formats:

- **Simple roles**: `web developer`, `data scientist`, `marketing manager`
- **With experience**: `senior developer with 5 years experience`
- **Entry level**: `junior analyst entry level`
- **Remote work**: `software engineer remote`
- **Industry specific**: `product manager fintech`

## 📊 Output Structure

Generated job descriptions include:

1. **Job Title & Basic Info** - Department, experience level, location, salary range
2. **Job Summary** - Concise overview of the role
3. **Key Responsibilities** - Numbered list of main duties
4. **Required Skills** - Technical and soft skills needed
5. **Preferred Skills** - Bonus qualifications
6. **Education Requirements** - Academic background needed
7. **Benefits Package** - Compensation and perks
8. **Company Culture** - Values and work environment

## 🔧 Configuration

The application uses optimal default settings:
- **Model**: `gpt-4o-mini` (fast and cost-effective)
- **Temperature**: `0.7` (balanced creativity)
- **API Key**: Automatically loaded from `.env` file

## 🆘 Troubleshooting

### Common Issues

**API Key Errors**
- Verify your OpenAI API key is correct
- Check account has sufficient credits
- Ensure `.env` file is in the correct directory

**Installation Issues**
- Update Python to 3.8+
- Use virtual environment for clean installation
- Check pip version compatibility

### Getting Help

1. Check OpenAI API status
2. Verify your API key permissions
3. Review error messages for specific issues
4. Try simpler input formats

## 📄 File Structure

```
HR agent/
├── job_description_agent.py    # Core agent logic
├── streamlit_app.py            # Web interface
├── requirements.txt            # Dependencies
├── .env                       # API key configuration
├── env_example.txt            # Environment template
└── README.md                  # This file
```

## 🙏 Acknowledgments

- Powered by [OpenAI](https://openai.com/) GPT models
- UI framework by [Streamlit](https://streamlit.io/)
- Data validation with [Pydantic](https://pydantic-docs.helpmanual.io/)

---

**Happy job description writing! 🎉**

