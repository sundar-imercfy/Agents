@echo off
echo Starting HR Job Description Generator...
echo.
echo Make sure you have:
echo 1. Python installed
echo 2. Dependencies installed: pip install -r requirements.txt
echo 3. OpenAI API key set in .env file
echo.
echo Starting web interface...
echo.
python -m streamlit run streamlit_app.py --server.headless true
pause