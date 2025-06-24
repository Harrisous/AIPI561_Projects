# 🚀 Quick Start Guide

🍽️ Food Instruction Generator with Ollama and Streamlit
=======================================================

PROJECT OVERVIEW:
This application uses Meta's Llama 3.2 11B Vision Instruct model hosted locally on Ollama to analyze food photos and provide detailed cooking instructions, recipes, and culinary guidance.

KEY FEATURES:
- 📸 Image Upload: Users can upload food photos through an intuitive interface
- 🤖 AI Analysis: Llama 3.2 Vision model analyzes the uploaded images
- 📝 Instruction Generation: Provides comprehensive cooking instructions including:
  * Dish identification and description
  * Estimated cooking time
  * Step-by-step cooking instructions
  * Key ingredients needed
  * Cooking tips and techniques
  * Serving suggestions
- 🎨 Beautiful UI: Modern, responsive Streamlit interface with custom styling
- ⚙️ Real-time Processing: Live connection status and model availability checking
- 🔧 Configurable: Adjustable parameters for model behavior

TECHNICAL ARCHITECTURE:
- Frontend: Streamlit web application
- Backend: Ollama API for model inference
- Model: Meta Llama 3.2 11B Vision Instruct (llama3.2-vision:11b)
- Image Processing: PIL for image handling and base64 encoding
- API Communication: HTTP requests to Ollama service

SETUP REQUIREMENTS:
- Ollama installed and running (ollama serve)
- Llama 3.2 Vision model pulled (ollama pull llama3.2-vision:11b)
- Python dependencies installed (see requirements.txt)
- Minimum 16GB RAM recommended for the 11B model

USAGE FLOW:
1. User uploads a food image
2. Image is processed and converted to base64
3. Prompt is sent to Ollama API with the image
4. Llama model analyzes the image and generates instructions
5. Results are displayed in a formatted, user-friendly interface


## For Windows Users

### Option 1: Automated Setup (Recommended)
1. Double-click `setup.bat` in the project folder
2. Wait for the setup to complete
3. Run the application: `streamlit run app.py`

### Option 2: Manual Setup
1. **Install Ollama:**
   ```cmd
   winget install Ollama.Ollama
   ```
   Or download from https://ollama.ai/download

2. **Install Python dependencies:**
   ```cmd
   pip install -r requirements.txt
   ```

3. **Start Ollama service:**
   ```cmd
   ollama serve
   ```

4. **Pull the model:**
   ```cmd
   ollama pull llama3.2-vision:11b
   ```

5. **Run the application:**
   ```cmd
   streamlit run app.py
   ```

## For macOS/Linux Users

### Option 1: Automated Setup
1. Make the script executable: `chmod +x setup.sh`
2. Run the setup: `./setup.sh`
3. Run the application: `streamlit run app.py`

### Option 2: Manual Setup
1. **Install Ollama:**
   ```bash
   # macOS
   brew install ollama
   
   # Linux
   curl -fsSL https://ollama.ai/install.sh | sh
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Start Ollama service:**
   ```bash
   ollama serve
   ```

4. **Pull the model:**
   ```bash
   ollama pull llama3.2-11b-vision-instruct
   ```

5. **Run the application:**
   ```bash
   streamlit run app.py
   ```

## 🎯 What You'll Get

After setup, you'll have:
- ✅ Ollama running locally
- ✅ Llama 3.2 11B Vision Instruct model downloaded
- ✅ Beautiful Streamlit UI for food instruction generation
- ✅ Real-time image analysis and cooking instructions

## 🌐 Access the Application

Once running, open your browser to: **http://localhost:8501**

## 📸 How to Use

1. **Upload a food photo** using the file uploader
2. **Click "Generate Instructions"** to analyze the image
3. **Get detailed cooking instructions** including:
   - Dish identification
   - Cooking time estimates
   - Step-by-step instructions
   - Ingredient suggestions
   - Cooking tips
   - Serving recommendations

## 🔧 Troubleshooting

### Model Not Found
```bash
ollama pull llama3.2-11b-vision-instruct
```

### Ollama Not Running
```bash
ollama serve
```

### Memory Issues
- Close other applications
- Ensure 16GB+ RAM available
- Consider using the 8B model variant

### Port Already in Use
If port 8501 is busy, Streamlit will automatically use the next available port.

## 📱 System Requirements

- **RAM:** 16GB+ recommended (8GB minimum)
- **Storage:** 15GB+ free space for the model
- **OS:** Windows 10+, macOS 10.15+, or Linux
- **Python:** 3.8+
- **Internet:** Required for initial model download 