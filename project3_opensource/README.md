# Video Summarization App - Windows Long Path Fix

This guide addresses the **Windows Long Path** issue that occurs when installing PyTorch and other dependencies on Windows systems.

## 🚨 The Problem

Windows has a 260-character limit for file paths. When installing PyTorch, the installation creates very long paths that exceed this limit, causing errors like:

```
ERROR: Could not install packages due to an OSError: [Errno 2] No such file or directory: 'C:\\Users\\...\\venv\\Lib\\site-packages\\torch\\include\\ATen\\ops\\...'
HINT: This error might have occurred since this system does not have Windows Long Path support enabled.
```

## 🔧 Solutions (Try in Order)

### Solution 1: Enable Long Path Support (Recommended)

1. **Open PowerShell as Administrator**
2. **Run this command:**
   ```powershell
   New-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem" -Name "LongPathsEnabled" -Value 1 -PropertyType DWORD -Force
   ```
3. **Restart your computer**
4. **Try the installation again**

### Solution 2: Use CPU-Only PyTorch (Easier)

Use the fixed setup script that installs CPU-only PyTorch:

```bash
setup_windows_fixed.bat
```

This avoids the long path issue by using smaller CPU-only packages.

### Solution 3: Manual Installation with CPU PyTorch

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install CPU-only PyTorch first
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cpu

# Install other dependencies
pip install streamlit ctransformers openai-whisper numpy pandas pillow moviepy pydub librosa soundfile transformers accelerate sentencepiece protobuf huggingface-hub requests tqdm
```

### Solution 4: Use Simplified Requirements

```bash
# Install from simplified requirements
pip install -r requirements_windows_simple.txt
```

### Solution 5: Move to Shorter Path

If the above solutions don't work, move your project to a shorter path:

```bash
# Instead of:
C:\Users\Harry\OneDrive - Duke University\Private\course\AIPI561 Operationalization\AIPI561_Projects\project3_opensource\

# Use:
C:\Projects\video-summarizer\
```

## 🛠️ Alternative Installation Methods

### Method A: Conda Installation

```bash
# Install Miniconda first, then:
conda create -n video-summarizer python=3.9
conda activate video-summarizer
conda install pytorch torchaudio cpuonly -c pytorch
pip install streamlit ctransformers openai-whisper
```

### Method B: Use Docker

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements_windows_simple.txt .
RUN pip install -r requirements_windows_simple.txt

COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app_windows.py"]
```

## 🔍 Troubleshooting Steps

1. **Check if long path support is enabled:**
   ```powershell
   reg query "HKLM\SYSTEM\CurrentControlSet\Control\FileSystem" /v LongPathsEnabled
   ```

2. **Clear pip cache:**
   ```bash
   pip cache purge
   ```

3. **Use shorter virtual environment path:**
   ```bash
   python -m venv C:\venv\video-summarizer
   ```

4. **Install with no cache:**
   ```bash
   pip install --no-cache-dir torch torchaudio
   ```

## 📋 System Requirements

- **Windows 10/11** (with latest updates)
- **Python 3.8+**
- **8GB+ RAM** (16GB recommended)
- **Administrator privileges** (for long path support)

## 🎯 Quick Fix Summary

**For immediate solution, use:**

```bash
# 1. Enable long path support (as admin)
# 2. Run the fixed setup script
setup_windows_fixed.bat

# 3. Or manually install CPU-only PyTorch
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cpu
```

## 🆘 Still Having Issues?

If none of the above solutions work:

1. **Use WSL2** (Windows Subsystem for Linux)
2. **Use a cloud development environment**
3. **Use the Docker version**
4. **Contact support with your specific error message**

## ✅ Success Indicators

You'll know it's working when:
- ✅ PyTorch installs without long path errors
- ✅ All dependencies install successfully
- ✅ `python test_windows.py` passes all tests
- ✅ `streamlit run app_windows.py` starts without errors

## 🎉 After Successful Installation

```bash
# Activate environment
venv\Scripts\activate

# Run the app
streamlit run app_windows.py

# Open browser to
http://localhost:8501
```

Happy video summarizing! 🎥✨ 