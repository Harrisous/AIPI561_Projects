"""
Configuration settings for the Video Summarization App
"""

import os
from pathlib import Path

# Base directories
BASE_DIR = Path(__file__).parent
MODELS_DIR = BASE_DIR / "models"
TEMP_DIR = BASE_DIR / "temp"

# Create directories if they don't exist
MODELS_DIR.mkdir(exist_ok=True)
TEMP_DIR.mkdir(exist_ok=True)

# LLM Configuration
LLM_CONFIG = {
    # Default model path (user should place their GGUF file here)
    "model_path": str(MODELS_DIR / "mixtral-8x7b-instruct-v0.1.Q3_K_M.gguf"),
    
    # Model parameters
    "n_ctx": 4096,  # Context window size
    "n_batch": 512,  # Batch size for prompt processing
    "n_gpu_layers": -1,  # -1 for all layers on GPU (requires CUDA-compatible GPU and ctransformers built with GPU support)
    "n_threads": 8,  # Number of CPU threads to use
    
    # Generation parameters
    "temperature": 0.7,
    "top_p": 0.9,
    "top_k": 40,
    "max_tokens": 1024,
    "repeat_penalty": 1.1,
}

# Whisper Configuration
WHISPER_CONFIG = {
    "model_name": "medium",  # Options: tiny, base, small, medium, large
    "language": None,  # None for auto-detection
    "task": "transcribe",
    "device": "cuda",  # 'cuda' for GPU, 'cpu' for CPU, or 'auto' for auto-detection
}

# Video Processing Configuration
VIDEO_CONFIG = {
    "max_duration": 3600,  # Maximum video duration in seconds (1 hour)
    "audio_format": "wav",
    "sample_rate": 16000,
    "chunk_duration": 30,  # Process audio in 30-second chunks
}

# Summarization Configuration
SUMMARY_CONFIG = {
    "max_length": 500,  # Maximum summary length in words
    "min_length": 100,  # Minimum summary length in words
    "style": "concise",  # Options: concise, detailed, bullet_points
}

# Streamlit UI Configuration
UI_CONFIG = {
    "page_title": "Video Summarization App",
    "page_icon": "🎥",
    "layout": "wide",
    "initial_sidebar_state": "expanded",
    "max_upload_size": 200,  # MB
}

# Prompt templates
PROMPTS = {
    "summarize": """You are a helpful assistant that creates concise and informative summaries. 
    
Please summarize the following text in a clear and structured way. Focus on the main points and key insights.

Text to summarize:
{text}

Please provide a summary that is:
- Clear and well-structured
- Captures the main points and key insights
- Approximately {max_length} words
- Written in a professional tone

Summary:""",

    "bullet_points": """You are a helpful assistant that creates structured summaries with bullet points.

Please summarize the following text using bullet points to highlight the key information.

Text to summarize:
{text}

Please provide a summary with:
- Main points as bullet points
- Key insights and takeaways
- Approximately {max_length} words total
- Clear and organized structure

Summary:""",
}

# File extensions
SUPPORTED_VIDEO_FORMATS = [
    ".mp4", ".avi", ".mov", ".mkv", ".wmv", ".flv", ".webm", ".m4v", ".3gp"
]

SUPPORTED_AUDIO_FORMATS = [
    ".wav", ".mp3", ".m4a", ".flac", ".ogg", ".aac"
]

# Error messages
ERROR_MESSAGES = {
    "ffmpeg_not_found": "FFmpeg not found. Please install FFmpeg and ensure it's in your PATH.",
    "model_not_found": "GGUF model not found. Please download a model and place it in the models/ directory.",
    "video_too_large": "Video file is too large. Maximum size is {} MB.",
    "unsupported_format": "Unsupported file format. Please use: {}",
    "processing_error": "Error processing video. Please check the file and try again.",
    "summarization_error": "Error generating summary. Please try again.",
}

# Success messages
SUCCESS_MESSAGES = {
    "video_processed": "Video processed successfully!",
    "summary_generated": "Summary generated successfully!",
    "file_downloaded": "File downloaded successfully!",
}

def get_model_path():
    """Get the path to the GGUF model file"""
    model_path = Path(LLM_CONFIG["model_path"])
    if not model_path.exists():
        # Try to find any GGUF file in the models directory
        gguf_files = list(MODELS_DIR.glob("*.gguf"))
        if gguf_files:
            return str(gguf_files[0])
        else:
            return None
    return str(model_path)

def validate_config():
    """Validate the configuration and return any issues"""
    issues = []
    
    # Check if FFmpeg is available
    try:
        import subprocess
        result = subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True)
        if result.returncode != 0:
            issues.append("FFmpeg not found or not working properly")
    except FileNotFoundError:
        issues.append("FFmpeg not found. Please install FFmpeg.")
    
    # Check if model exists
    model_path = get_model_path()
    if not model_path:
        issues.append("No GGUF model found in models/ directory")
    
    return issues 