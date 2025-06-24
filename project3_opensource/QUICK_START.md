# Quick Start Guide

Get your video summarization app running in 5 minutes!

## Prerequisites

- **Python 3.8+** installed
- **FFmpeg** installed (for video processing)
- **8GB+ RAM** (for LLM inference)
- **GGUF model file** (download one from the links below)

## Step 1: Install FFmpeg

### Windows
```bash
# Using chocolatey (recommended)
choco install ffmpeg

# Or download from https://ffmpeg.org/download.html

# or use winget
winget install FFmpeg

### macOS
```bash
brew install ffmpeg
```

### Linux
```bash
sudo apt update && sudo apt install ffmpeg  # Ubuntu/Debian
sudo yum install ffmpeg                      # CentOS/RHEL
```

## Step 2: Download a GGUF Model

Download one of these recommended models and place it in the `models/` directory:

- **Mistral 7B Instruct** (Recommended): [Download](https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.2-GGUF/resolve/main/mistral-7b-instruct-v0.2.Q4_K_M.gguf)
- **Llama 2 7B Chat**: [Download](https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF/resolve/main/llama-2-7b-chat.Q4_K_M.gguf)
- **Phi-2** (Lightweight): [Download](https://huggingface.co/TheBloke/phi-2-GGUF/resolve/main/phi-2.Q4_K_M.gguf)

## Step 3: Setup the Application

### Option A: Automated Setup (Recommended)

**Windows:**
```bash
setup.bat
```

**macOS/Linux:**
```bash
chmod +x setup.sh
./setup.sh
```

### Option B: Manual Setup

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create directories
mkdir models
mkdir temp
```

## Step 4: Run the Application

```bash
# Make sure virtual environment is activated
streamlit run app.py
```

The app will open at: **http://localhost:8501**

## Step 5: Use the Application

1. **Upload a video** (MP4, AVI, MOV, etc.)
2. **Click "Process Video"** to extract audio and convert to text
3. **Click "Generate Summary"** to create a summary using the local LLM
4. **Download results** as text files

## Troubleshooting

### Common Issues

**"FFmpeg not found"**
- Install FFmpeg and ensure it's in your PATH
- Restart your terminal after installation

**"No GGUF model found"**
- Download a GGUF model and place it in the `models/` directory
- Make sure the file has a `.gguf` extension

**"Out of memory"**
- Use a smaller model (Phi-2 instead of Mistral 7B)
- Close other applications to free up RAM
- Reduce batch size in `config.py`

**"CUDA errors"**
- Install compatible GPU drivers
- Set `n_gpu_layers: 0` in `config.py` for CPU-only mode

### Performance Tips

- **GPU acceleration**: Set `n_gpu_layers: -1` in `config.py` if you have a compatible GPU
- **Model size**: Use smaller models for faster inference
- **Whisper model**: Use "tiny" or "base" for faster transcription
- **Summary length**: Reduce max length for faster generation

## Configuration

Edit `config.py` to customize:

```python
# LLM settings
LLM_CONFIG = {
    "n_gpu_layers": -1,  # -1 for GPU, 0 for CPU
    "n_threads": 8,      # Number of CPU threads
    "temperature": 0.7,  # Creativity level
}

# Summary settings
SUMMARY_CONFIG = {
    "max_length": 500,   # Maximum summary length
    "style": "concise",  # Summary style
}
```

## Next Steps

- Try different video formats and lengths
- Experiment with different summary styles
- Adjust model parameters for your use case
- Check out the full documentation in `README.md`

## Support

If you encounter issues:
1. Check the troubleshooting section above
2. Verify all prerequisites are installed
3. Check the console output for error messages
4. Ensure you have sufficient system resources

Happy video summarizing! 🎥✨ 