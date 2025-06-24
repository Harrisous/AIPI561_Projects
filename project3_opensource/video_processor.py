"""
Video processing module for extracting audio and converting to text
"""

import os
import tempfile
import subprocess
from pathlib import Path
from typing import Optional, Tuple, List
import whisper
import torch
import numpy as np
import logging

from config import (
    WHISPER_CONFIG, 
    VIDEO_CONFIG, 
    SUPPORTED_VIDEO_FORMATS,
    ERROR_MESSAGES,
    TEMP_DIR
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VideoProcessor:
    """Handles video processing, audio extraction, and speech-to-text conversion"""
    
    def __init__(self):
        self.whisper_model = None
        self._load_whisper_model()
    
    def _load_whisper_model(self):
        """Load the Whisper model"""
        try:
            logger.info(f"Loading Whisper model: {WHISPER_CONFIG['model_name']} on device: {WHISPER_CONFIG['device']}")
            self.whisper_model = whisper.load_model(
                WHISPER_CONFIG['model_name'],
                device=WHISPER_CONFIG['device']
            )
            logger.info("Whisper model loaded successfully")
        except Exception as e:
            logger.error(f"Error loading Whisper model: {e}")
            raise
    
    def validate_video_file(self, file_path: str) -> Tuple[bool, str]:
        """Validate if the uploaded file is a supported video format"""
        file_path = Path(file_path)
        
        # Check if file exists
        if not file_path.exists():
            return False, "File does not exist"
        
        # Check file extension
        if file_path.suffix.lower() not in SUPPORTED_VIDEO_FORMATS:
            return False, ERROR_MESSAGES["unsupported_format"].format(
                ", ".join(SUPPORTED_VIDEO_FORMATS)
            )
        
        # Check file size
        file_size_mb = file_path.stat().st_size / (1024 * 1024)
        if file_size_mb > VIDEO_CONFIG["max_duration"]:
            return False, ERROR_MESSAGES["video_too_large"].format(
                VIDEO_CONFIG["max_duration"]
            )
        
        return True, "File is valid"
    
    def extract_audio_from_video(self, video_path: str) -> str:
        """Extract audio from video file using FFmpeg (optionally, add GPU acceleration flags for video decode if needed)"""
        try:
            # Create temporary audio file
            audio_filename = f"audio_{Path(video_path).stem}.{VIDEO_CONFIG['audio_format']}"
            audio_path = TEMP_DIR / audio_filename
            
            # FFmpeg command to extract audio
            cmd = [
                "ffmpeg",
                # Optional: Uncomment the next line to use NVIDIA GPU for video decode (if available)
                # "-hwaccel", "cuda",
                "-i", video_path,
                "-vn",  # No video
                "-acodec", "pcm_s16le",  # Audio codec
                "-ar", str(VIDEO_CONFIG["sample_rate"]),  # Sample rate
                "-ac", "1",  # Mono audio
                "-y",  # Overwrite output file
                str(audio_path)
            ]
            
            logger.info(f"Extracting audio from video: {video_path}")
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode != 0:
                logger.error(f"FFmpeg error: {result.stderr}")
                raise Exception("Failed to extract audio from video")
            
            logger.info(f"Audio extracted successfully: {audio_path}")
            return str(audio_path)
            
        except FileNotFoundError:
            raise Exception(ERROR_MESSAGES["ffmpeg_not_found"])
        except Exception as e:
            logger.error(f"Error extracting audio: {e}")
            raise
    
    def get_video_info(self, video_path: str) -> dict:
        """Get video information using FFmpeg"""
        try:
            cmd = [
                "ffmpeg",
                "-i", video_path,
                "-f", "null",
                "-"
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            # Parse duration from stderr output
            duration = None
            for line in result.stderr.split('\n'):
                if "Duration:" in line:
                    time_str = line.split("Duration: ")[1].split(",")[0].strip()
                    # Convert HH:MM:SS.ms to seconds
                    time_parts = time_str.split(':')
                    duration = (
                        int(time_parts[0]) * 3600 + 
                        int(time_parts[1]) * 60 + 
                        float(time_parts[2])
                    )
                    break
            
            return {
                "duration": duration,
                "path": video_path,
                "filename": Path(video_path).name
            }
            
        except Exception as e:
            logger.error(f"Error getting video info: {e}")
            return {"duration": None, "path": video_path, "filename": Path(video_path).name}
    
    def transcribe_audio(self, audio_path: str) -> str:
        """Transcribe audio to text using Whisper"""
        try:
            logger.info(f"Transcribing audio: {audio_path}")
            
            # Load audio and transcribe
            result = self.whisper_model.transcribe(
                audio_path,
                language=WHISPER_CONFIG["language"],
                task=WHISPER_CONFIG["task"]
            )
            
            transcription = result["text"].strip()
            logger.info(f"Transcription completed. Length: {len(transcription)} characters")
            
            return transcription
            
        except Exception as e:
            logger.error(f"Error transcribing audio: {e}")
            raise
    
    def process_video(self, video_path: str) -> dict:
        """Complete video processing pipeline"""
        try:
            # Validate video file
            is_valid, message = self.validate_video_file(video_path)
            if not is_valid:
                raise Exception(message)
            
            # Get video information
            video_info = self.get_video_info(video_path)
            
            # Extract audio
            audio_path = self.extract_audio_from_video(video_path)
            
            # Transcribe audio
            transcription = self.transcribe_audio(audio_path)
            
            # Clean up temporary audio file
            try:
                os.remove(audio_path)
                logger.info(f"Cleaned up temporary audio file: {audio_path}")
            except:
                pass
            
            return {
                "success": True,
                "video_info": video_info,
                "transcription": transcription,
                "word_count": len(transcription.split()),
                "audio_path": audio_path
            }
            
        except Exception as e:
            logger.error(f"Error processing video: {e}")
            return {
                "success": False,
                "error": str(e),
                "video_info": None,
                "transcription": None,
                "word_count": 0,
                "audio_path": None
            }
    
    def chunk_transcription(self, transcription: str, chunk_size: int = 1000) -> List[str]:
        """Split transcription into chunks for processing"""
        words = transcription.split()
        chunks = []
        
        for i in range(0, len(words), chunk_size):
            chunk = " ".join(words[i:i + chunk_size])
            chunks.append(chunk)
        
        return chunks

def check_ffmpeg_availability() -> bool:
    """Check if FFmpeg is available in the system"""
    try:
        result = subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True)
        return result.returncode == 0
    except FileNotFoundError:
        return False

def get_available_whisper_models() -> List[str]:
    """Get list of available Whisper model sizes"""
    return ["tiny", "base", "small", "medium", "large"]

def estimate_processing_time(video_duration: float) -> float:
    """Estimate processing time based on video duration"""
    # Rough estimates: 1 second of video takes ~0.5 seconds to process
    return video_duration * 0.5 