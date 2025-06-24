@echo off
echo 🚀 Food Instruction Generator Setup
echo ====================================

echo.
echo 📦 Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python from https://python.org
    pause
    exit /b 1
)
echo ✅ Python is installed

echo.
echo 📦 Installing Python dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ Failed to install Python dependencies
    pause
    exit /b 1
)
echo ✅ Python dependencies installed

echo.
echo 📦 Checking Ollama installation...
ollama --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Ollama is not installed
    echo Installing Ollama...
    winget install Ollama.Ollama
    if errorlevel 1 (
        echo ❌ Failed to install Ollama via winget
        echo Please download and install manually from https://ollama.ai/download
        pause
        exit /b 1
    )
    echo ✅ Ollama installed successfully
) else (
    echo ✅ Ollama is already installed
)

echo.
echo 🚀 Starting Ollama service...
start /B ollama serve
timeout /t 5 /nobreak >nul

echo.
echo 📥 Pulling Llama 3.2 11B Vision Instruct model...
echo This may take several minutes depending on your internet connection...
ollama pull llama3.2-vision:11b
if errorlevel 1 (
    echo ❌ Failed to pull the model
    pause
    exit /b 1
)
echo ✅ Model pulled successfully

echo.
echo 🎉 Setup completed successfully!
echo.
echo 📋 To run the application:
echo 1. Make sure Ollama is running: ollama serve
echo 2. Run: streamlit run app.py
echo 3. Open your browser to http://localhost:8501
echo.
pause 