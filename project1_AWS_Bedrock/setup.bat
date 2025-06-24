@echo off
echo ========================================
echo AWS Bedrock Food Instruction Generator
echo ========================================
echo.

echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://python.org
    pause
    exit /b 1
)

echo Python found!
echo.

echo Checking AWS CLI installation...
aws --version >nul 2>&1
if errorlevel 1 (
    echo WARNING: AWS CLI is not installed
    echo Please install AWS CLI from https://aws.amazon.com/cli/
    echo.
    echo After installation, run: aws configure
    echo.
    pause
) else (
    echo AWS CLI found!
    echo.
    echo Checking AWS credentials...
    aws sts get-caller-identity >nul 2>&1
    if errorlevel 1 (
        echo WARNING: AWS credentials not configured
        echo Please run: aws configure
        echo.
        pause
    ) else (
        echo AWS credentials configured!
    )
)

echo.
echo Creating virtual environment...
python -m venv .venv
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment
    pause
    exit /b 1
)

echo Activating virtual environment...
call .venv\Scripts\activate.bat

echo Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo ========================================
echo Setup completed successfully!
echo ========================================
echo.
echo Next steps:
echo 1. Ensure you have AWS Bedrock access
echo 2. Request access to meta.llama3.2-90b-vision-instruct-v1:0
echo 3. Run: streamlit run app.py
echo.
echo For more information, see README.md
echo.
pause 