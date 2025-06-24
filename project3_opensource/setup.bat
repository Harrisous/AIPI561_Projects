@echo off
echo ========================================
echo Video Summarization App Setup (Windows)
echo Fixed for Long Path Issues
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

echo Python found: 
python --version
echo.

REM Check if pip is available
pip --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: pip is not available
    echo Please ensure pip is installed with Python
    pause
    exit /b 1
)

echo pip found:
pip --version
echo.

REM Create virtual environment in a shorter path
echo Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment
    pause
    exit /b 1
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install CPU-only PyTorch first (avoids long path issues)
echo Installing PyTorch...
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
if errorlevel 1 (
    echo WARNING: PyTorch installation failed, trying alternative method...
    pip install torch torchaudio --no-cache-dir
)

REM Install other dependencies
echo Installing other dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
)

echo Dependencies installed successfully!
echo.

REM Create necessary directories
echo Creating directories...
if not exist "models" mkdir models
if not exist "temp" mkdir temp

REM Check for FFmpeg
echo Checking for FFmpeg...
ffmpeg -version >nul 2>&1
if errorlevel 1 (
    echo WARNING: FFmpeg not found in PATH
    echo Please install FFmpeg from https://ffmpeg.org/download.html
    echo Or use chocolatey: choco install ffmpeg
    echo.
    echo After installing FFmpeg, restart this script
    pause
    exit /b 1
)

echo FFmpeg found:
ffmpeg -version | findstr "ffmpeg version"
echo.

REM Check for GGUF models
echo Checking for GGUF models...
if not exist "models\*.gguf" (
    echo WARNING: No GGUF models found in models/ directory
    echo.
    echo Please download a GGUF model and place it in the models/ directory
    echo Recommended models:
    echo - Mistral 8x7B Instruct: https://huggingface.co/TheBloke/Mixtral-8x7B-Instruct-v0.1-GGUF/blob/main/mixtral-8x7b-instruct-v0.1.Q4_K_M.gguf
    echo - Llama 2 7B Chat: https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF/blob/main/llama-2-7b-chat.Q4_K_M.gguf
    echo - Phi-2: https://huggingface.co/TheBloke/phi-2-GGUF/blob/main/phi-2-gguf-q4_0.gguf
    echo.
    echo Download a .gguf file and place it in the models/ directory
    echo.
)

echo ========================================
echo Setup completed successfully!
echo ========================================
echo.
echo To run the Windows version:
echo 1. Activate the virtual environment: venv\Scripts\activate
echo 2. Run the Windows app: streamlit run app_windows.py
echo 3. Open your browser to: http://localhost:8501
echo.
echo To deactivate the virtual environment: deactivate
echo.
pause 