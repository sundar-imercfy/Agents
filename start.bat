@echo off
echo Starting Job Description Agent...
echo.
echo Make sure you have:
echo 1. Python installed
echo 2. Dependencies installed (pip install -r requirements.txt)
echo 3. OpenAI API key set in .env file
echo.
echo Starting Streamlit web interface...
echo.
streamlit run streamlit_app.py
pause
