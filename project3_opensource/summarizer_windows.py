"""
Text summarization using llama-cpp-python and GGUF models
Windows-compatible version (no compilation required)
"""

import os
import time
import re
from typing import Optional, List, Dict, Any
from llama_cpp import Llama
import logging

from config import (
    LLM_CONFIG, 
    SUMMARY_CONFIG, 
    PROMPTS, 
    ERROR_MESSAGES,
    get_model_path
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TextSummarizer:
    """Handles text summarization using llama-cpp-python and GGUF models"""
    
    def __init__(self, model_path: Optional[str] = None):
        self.model_path = model_path or get_model_path()
        self.llm = None
        self.use_fallback = False
        self._load_model()
    
    def _load_model(self):
        """Load the GGUF model using llama-cpp-python"""
        try:
            if not self.model_path or not os.path.exists(self.model_path):
                logger.warning("Model file not found, using fallback summarization")
                self.use_fallback = True
                return
            
            logger.info(f"Loading GGUF model: {self.model_path}")
            
            self.llm = Llama(
                model_path=self.model_path,
                n_ctx=LLM_CONFIG["n_ctx"],
                n_threads=LLM_CONFIG["n_threads"],
                n_gpu_layers=LLM_CONFIG["n_gpu_layers"]
            )
            
            logger.info(f"GGUF model loaded successfully with llama-cpp-python")
            
        except Exception as e:
            logger.error(f"Error loading GGUF model: {e}")
            logger.info("Using fallback summarization method")
            self.use_fallback = True
    
    def _extractive_summarize(self, text: str, max_length: int = 500) -> str:
        """Fallback extractive summarization using sentence scoring, output as bullet points"""
        try:
            # Split text into sentences
            sentences = re.split(r'[.!?]+', text)
            sentences = [s.strip() for s in sentences if s.strip()]
            
            if len(sentences) <= 3:
                return '\n'.join([f"- {s}" for s in sentences])
            
            # Simple scoring based on word frequency
            word_freq = {}
            for sentence in sentences:
                words = re.findall(r'\b\w+\b', sentence.lower())
                for word in words:
                    if len(word) > 3:  # Skip short words
                        word_freq[word] = word_freq.get(word, 0) + 1
            
            # Score sentences
            sentence_scores = []
            for sentence in sentences:
                words = re.findall(r'\b\w+\b', sentence.lower())
                score = sum(word_freq.get(word, 0) for word in words if len(word) > 3)
                sentence_scores.append((score, sentence))
            
            # Sort by score and take top sentences
            sentence_scores.sort(reverse=True)
            
            # Select sentences until we reach max_length
            selected_sentences = []
            current_length = 0
            
            for score, sentence in sentence_scores:
                if current_length + len(sentence.split()) <= max_length:
                    selected_sentences.append(sentence)
                    current_length += len(sentence.split())
                else:
                    break
            
            # Sort back to original order
            selected_sentences.sort(key=lambda x: sentences.index(x))
            
            # Output as bullet points
            summary = '\n'.join([f"- {s}" for s in selected_sentences])
            return summary
            
        except Exception as e:
            logger.error(f"Error in extractive summarization: {e}")
            # Return first few sentences as fallback, as bullet points
            sentences = re.split(r'[.!?]+', text)
            sentences = [s.strip() for s in sentences if s.strip()]
            return '\n'.join([f"- {s}" for s in sentences[:3]])
    
    def _create_prompt(self, text: str, style: str = "concise", max_length: int = None) -> str:
        """Create a prompt for summarization based on style (always use bullet points)"""
        max_length = max_length or SUMMARY_CONFIG["max_length"]
        # Always use bullet point prompt
        return PROMPTS["bullet_points"].format(
            text=text,
            max_length=max_length
        )
    
    def _chunk_text(self, text: str, max_chunk_size: int = 2000) -> List[str]:
        """Split text into manageable chunks"""
        words = text.split()
        chunks = []
        
        current_chunk = []
        current_size = 0
        
        for word in words:
            word_size = len(word) + 1  # +1 for space
            
            if current_size + word_size > max_chunk_size and current_chunk:
                chunks.append(" ".join(current_chunk))
                current_chunk = [word]
                current_size = word_size
            else:
                current_chunk.append(word)
                current_size += word_size
        
        if current_chunk:
            chunks.append(" ".join(current_chunk))
        
        return chunks
    
    def summarize_text(self, text: str, style: str = "concise", max_length: int = None) -> Dict[str, Any]:
        """Generate a summary of the given text"""
        try:
            if not text.strip():
                return {
                    "success": False,
                    "error": "No text provided for summarization",
                    "summary": "",
                    "word_count": 0,
                    "processing_time": 0
                }
            
            start_time = time.time()
            
            # Determine max length
            max_length = max_length or SUMMARY_CONFIG["max_length"]
            
            # Use fallback if LLM is not available
            if self.use_fallback or self.llm is None:
                logger.info("Using fallback extractive summarization")
                summary = self._extractive_summarize(text, max_length)
                processing_time = time.time() - start_time
                word_count = len(summary.split())
                
                return {
                    "success": True,
                    "summary": summary,
                    "word_count": word_count,
                    "processing_time": processing_time,
                    "style": "extractive",  # Override style for fallback
                    "max_length": max_length,
                    "method": "fallback_extractive"
                }
            
            # If text is short enough, summarize directly
            if len(text.split()) <= max_length * 2:
                prompt = self._create_prompt(text, style, max_length)
                
                logger.info("Generating summary for short text")
                response = self.llm(
                    prompt,
                    max_tokens=LLM_CONFIG["max_tokens"],
                    temperature=LLM_CONFIG["temperature"]
                )
                
                summary = response['choices'][0]['text'].strip()
                
            else:
                # For longer texts, use chunking strategy
                logger.info("Processing long text with chunking strategy")
                summary = self._summarize_long_text(text, style, max_length)
            
            processing_time = time.time() - start_time
            word_count = len(summary.split())
            
            logger.info(f"Summary generated successfully. Words: {word_count}, Time: {processing_time:.2f}s")
            
            return {
                "success": True,
                "summary": summary,
                "word_count": word_count,
                "processing_time": processing_time,
                "style": style,
                "max_length": max_length,
                "method": "llama_cpp"
            }
            
        except Exception as e:
            logger.error(f"Error generating summary: {e}")
            # Try fallback if LLM failed
            try:
                logger.info("LLM failed, trying fallback summarization")
                summary = self._extractive_summarize(text, max_length or SUMMARY_CONFIG["max_length"])
                processing_time = time.time() - start_time
                word_count = len(summary.split())
                
                return {
                    "success": True,
                    "summary": summary,
                    "word_count": word_count,
                    "processing_time": processing_time,
                    "style": "extractive",
                    "max_length": max_length or SUMMARY_CONFIG["max_length"],
                    "method": "fallback_extractive"
                }
            except Exception as fallback_error:
                logger.error(f"Fallback summarization also failed: {fallback_error}")
                return {
                    "success": False,
                    "error": f"Both LLM and fallback summarization failed. LLM error: {e}, Fallback error: {fallback_error}",
                    "summary": "",
                    "word_count": 0,
                    "processing_time": 0
                }
    
    def _summarize_long_text(self, text: str, style: str, max_length: int) -> str:
        """Summarize long text using chunking strategy"""
        # Split text into chunks
        chunks = self._chunk_text(text)
        
        if len(chunks) == 1:
            # Single chunk, summarize directly
            return self.summarize_text(chunks[0], style, max_length)["summary"]
        
        # Summarize each chunk
        chunk_summaries = []
        for i, chunk in enumerate(chunks):
            logger.info(f"Summarizing chunk {i+1}/{len(chunks)}")
            
            chunk_result = self.summarize_text(
                chunk, 
                style="concise", 
                max_length=max_length // len(chunks)
            )
            
            if chunk_result["success"]:
                chunk_summaries.append(chunk_result["summary"])
            else:
                logger.warning(f"Failed to summarize chunk {i+1}: {chunk_result['error']}")
        
        if not chunk_summaries:
            raise Exception("Failed to summarize any chunks")
        
        # Combine chunk summaries
        combined_text = " ".join(chunk_summaries)
        
        # Create final summary
        final_prompt = self._create_prompt(combined_text, style, max_length)
        
        response = self.llm(
            final_prompt,
            max_tokens=LLM_CONFIG["max_tokens"],
            temperature=LLM_CONFIG["temperature"]
        )
        
        return response['choices'][0]['text'].strip()
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the loaded model"""
        try:
            return {
                "model_path": self.model_path,
                "model_name": os.path.basename(self.model_path),
                "model_size_mb": os.path.getsize(self.model_path) / (1024 * 1024),
                "context_size": LLM_CONFIG["n_ctx"],
                "batch_size": LLM_CONFIG["n_batch"],
                "gpu_layers": LLM_CONFIG["n_gpu_layers"],
                "threads": LLM_CONFIG["n_threads"],
                "backend": "llama-cpp"
            }
        except Exception as e:
            logger.error(f"Error getting model info: {e}")
            return {"error": str(e)}
    
    def test_model(self) -> Dict[str, Any]:
        """Test the model with a simple prompt"""
        try:
            if self.use_fallback or self.llm is None:
                # Test fallback summarization
                test_text = "This is a test text for summarization. It contains multiple sentences to test the extractive summarization method. The fallback method should work even without the LLM model."
                
                summary = self._extractive_summarize(test_text, 50)
                
                return {
                    "success": True,
                    "response": summary,
                    "model_working": False,
                    "method": "fallback_extractive",
                    "note": "Using fallback summarization - LLM model not available"
                }
            
            test_prompt = "Hello, how are you?"
            
            response = self.llm(
                test_prompt,
                max_tokens=50,
                temperature=0.7
            )
            
            return {
                "success": True,
                "response": response['choices'][0]['text'].strip(),
                "model_working": True,
                "method": "llama_cpp"
            }
            
        except Exception as e:
            logger.error(f"Model test failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "model_working": False
            }

def get_available_summary_styles() -> List[str]:
    """Get available summary styles"""
    return ["concise", "detailed", "bullet_points"]

def estimate_summary_length(text_length: int, style: str = "concise") -> int:
    """Estimate summary length based on input text length and style"""
    if style == "bullet_points":
        ratio = 0.3
    elif style == "detailed":
        ratio = 0.5
    else:  # concise
        ratio = 0.25
    
    estimated_length = int(text_length * ratio)
    return max(SUMMARY_CONFIG["min_length"], 
               min(estimated_length, SUMMARY_CONFIG["max_length"]))

def validate_summary_quality(summary: str, original_text: str) -> Dict[str, Any]:
    """Basic validation of summary quality"""
    if not summary or not original_text:
        return {"valid": False, "reason": "Empty text"}
    
    summary_words = len(summary.split())
    original_words = len(original_text.split())
    
    # Check if summary is too short
    if summary_words < SUMMARY_CONFIG["min_length"]:
        return {"valid": False, "reason": "Summary too short"}
    
    # Check if summary is too long
    if summary_words > SUMMARY_CONFIG["max_length"]:
        return {"valid": False, "reason": "Summary too long"}
    
    # Check compression ratio
    compression_ratio = summary_words / original_words
    if compression_ratio > 0.8:
        return {"valid": False, "reason": "Insufficient compression"}
    
    return {
        "valid": True,
        "compression_ratio": compression_ratio,
        "summary_words": summary_words,
        "original_words": original_words
    } 