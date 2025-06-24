@echo off
REM Setup and run the Bedrock Memory Chatbot
python -m venv venv
call venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py 