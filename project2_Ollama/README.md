# Food Instruction Generator with Ollama and Streamlit

This project uses Meta's Llama 3.2 11B Vision Instruct model hosted on Ollama to provide cooking instructions based on uploaded food photos.

## Prerequisites

### 1. Install Ollama

**Windows:**
```bash
# Download and install from https://ollama.ai/download
# Or use winget
winget install Ollama.Ollama
```

**macOS:**
```bash
# Download and install from https://ollama.ai/download
# Or use Homebrew
brew install ollama
```

**Linux:**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

### 2. Pull the Llama 3.2 11B Vision Instruct Model

After installing Ollama, pull the model:
```bash
ollama pull llama3.2-11b-vision-instruct
```

**Note:** This model is approximately 11GB and may take some time to download depending on your internet connection.

### 3. Install Python Dependencies

```bash
pip install -r requirements.txt
```

## Usage

### 1. Start Ollama Service

Make sure Ollama is running:
```bash
ollama serve
```

### 2. Run the Streamlit Application

```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`.

## Features

- Upload food photos through a user-friendly interface
- Get detailed cooking instructions and recipe suggestions
- Real-time processing with the Llama 3.2 Vision model
- Responsive design for various screen sizes

## Troubleshooting

### Model Not Found
If you get an error about the model not being found:
```bash
# Check available models
ollama list

# Pull the model again if needed
ollama pull llama3.2-11b-vision-instruct
```

### Memory Issues
The 11B model requires significant RAM (at least 16GB recommended). If you experience memory issues:
- Close other applications
- Consider using a smaller model variant
- Ensure you have sufficient swap space

### Ollama Connection Issues
If the app can't connect to Ollama:
- Ensure Ollama is running: `ollama serve`
- Check if the service is accessible at `http://localhost:11434`
- Restart the Ollama service if needed

## Project Structure

```
project2_Ollama/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
└── README.md          # This file
``` 