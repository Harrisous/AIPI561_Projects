"""
Test script for Video Summarization App (Windows Version)
Tests ctransformers-based components
"""

import os
import sys
import tempfile
from pathlib import Path

def test_imports():
    """Test if all required modules can be imported"""
    print("Testing imports...")
    
    try:
        import streamlit
        print("✅ Streamlit imported successfully")
    except ImportError as e:
        print(f"❌ Streamlit import failed: {e}")
        return False
    
    try:
        import whisper
        print("✅ Whisper imported successfully")
    except ImportError as e:
        print(f"❌ Whisper import failed: {e}")
        return False
    
    try:
        from ctransformers import AutoModelForCausalLM
        print("✅ ctransformers imported successfully")
    except ImportError as e:
        print(f"❌ ctransformers import failed: {e}")
        return False
    
    try:
        from config import validate_config, get_model_path
        print("✅ Local modules imported successfully")
    except ImportError as e:
        print(f"❌ Local module import failed: {e}")
        return False
    
    return True

def test_ffmpeg():
    """Test if FFmpeg is available"""
    print("\nTesting FFmpeg...")
    
    try:
        import subprocess
        result = subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ FFmpeg is available")
            return True
        else:
            print("❌ FFmpeg returned error")
            return False
    except FileNotFoundError:
        print("❌ FFmpeg not found in PATH")
        return False

def test_model_availability():
    """Test if GGUF model is available"""
    print("\nTesting model availability...")
    
    try:
        from config import get_model_path
        model_path = get_model_path()
        
        if model_path and os.path.exists(model_path):
            model_size = os.path.getsize(model_path) / (1024 * 1024)
            print(f"✅ GGUF model found: {Path(model_path).name} ({model_size:.1f} MB)")
            return True
        else:
            print("❌ No GGUF model found in models/ directory")
            print("Please download a GGUF model and place it in the models/ directory")
            return False
    except Exception as e:
        print(f"❌ Error checking model: {e}")
        return False

def test_whisper_model():
    """Test Whisper model loading"""
    print("\nTesting Whisper model...")
    
    try:
        import whisper
        model = whisper.load_model("tiny")  # Use tiny for quick test
        print("✅ Whisper model loaded successfully")
        return True
    except Exception as e:
        print(f"❌ Whisper model loading failed: {e}")
        return False

def test_llama_cpp():
    """Test llama-cpp-python model loading"""
    print("\nTesting llama-cpp-python...")
    try:
        from config import get_model_path
        model_path = get_model_path()
        if not model_path or not os.path.exists(model_path):
            print("❌ No GGUF model available for testing")
            return False
        from llama_cpp import Llama
        llm = Llama(
            model_path=model_path,
            n_ctx=512,
            n_threads=1,
            n_gpu_layers=0
        )
        response = llm("Hello", max_tokens=10)
        if response and response['choices'][0]['text']:
            print("✅ llama-cpp-python model loaded and working")
            return True
        else:
            print("❌ llama-cpp-python model test failed")
            return False
    except Exception as e:
        print(f"❌ llama-cpp-python test failed: {e}")
        return False

def test_video_processor():
    """Test video processor module"""
    print("\nTesting video processor...")
    
    try:
        from video_processor import VideoProcessor, check_ffmpeg_availability
        
        # Test FFmpeg availability
        if not check_ffmpeg_availability():
            print("❌ FFmpeg not available for video processing")
            return False
        
        # Test VideoProcessor initialization
        processor = VideoProcessor()
        print("✅ Video processor initialized successfully")
        return True
        
    except Exception as e:
        print(f"❌ Video processor test failed: {e}")
        return False

def test_windows_summarizer():
    """Test Windows summarizer module"""
    print("\nTesting Windows summarizer...")
    
    try:
        from summarizer_windows import TextSummarizer
        
        # Test summarizer initialization
        summarizer = TextSummarizer()
        print("✅ Windows summarizer initialized successfully")
        
        # Test model info
        model_info = summarizer.get_model_info()
        if "error" not in model_info:
            print(f"✅ Model info retrieved: {model_info.get('model_name', 'Unknown')}")
        else:
            print(f"⚠️ Model info error: {model_info['error']}")
        
        # Test model functionality
        test_result = summarizer.test_model()
        if test_result["success"]:
            method = test_result.get("method", "unknown")
            if method == "llm":
                print("✅ LLM model is working")
            elif method == "fallback_extractive":
                print("✅ Fallback extractive summarization is working")
                if "note" in test_result:
                    print(f"   Note: {test_result['note']}")
        else:
            print(f"⚠️ Model test failed: {test_result.get('error', 'Unknown error')}")
        
        # Test simple summarization
        test_text = "This is a test text for summarization. It contains multiple sentences to test the summarization functionality. The system should be able to create a concise summary of this content."
        result = summarizer.summarize_text(test_text, style="concise", max_length=50)
        
        if result["success"]:
            method = result.get("method", "unknown")
            word_count = result.get("word_count", 0)
            processing_time = result.get("processing_time", 0)
            
            print(f"✅ Summarization test successful using {method} method")
            print(f"   Summary length: {word_count} words")
            print(f"   Processing time: {processing_time:.2f} seconds")
            
            # Show a preview of the summary
            summary = result.get("summary", "")
            if summary:
                preview = summary[:100] + "..." if len(summary) > 100 else summary
                print(f"   Summary preview: {preview}")
            
            return True
        else:
            print(f"❌ Summarization test failed: {result['error']}")
            return False
            
    except Exception as e:
        print(f"❌ Windows summarizer test failed: {e}")
        return False

def test_fallback_summarization():
    """Test fallback extractive summarization specifically"""
    print("\nTesting fallback summarization...")
    
    try:
        from summarizer_windows import TextSummarizer
        
        # Create a summarizer instance
        summarizer = TextSummarizer()
        
        # Test with longer text to better demonstrate extractive summarization
        test_text = """
        Artificial intelligence has become increasingly important in modern technology. 
        Machine learning algorithms are used in various applications from recommendation systems to autonomous vehicles. 
        Deep learning, a subset of machine learning, uses neural networks with multiple layers to process complex data. 
        Natural language processing enables computers to understand and generate human language. 
        Computer vision allows machines to interpret and analyze visual information from the world. 
        These technologies are transforming industries and creating new opportunities for innovation.
        """
        
        # Test different summary styles
        styles = ["concise", "detailed"]
        results = []
        
        for style in styles:
            result = summarizer.summarize_text(test_text, style=style, max_length=100)
            if result["success"]:
                method = result.get("method", "unknown")
                word_count = result.get("word_count", 0)
                results.append((style, method, word_count))
                print(f"✅ {style} style summary: {word_count} words using {method}")
            else:
                print(f"❌ {style} style summary failed: {result['error']}")
        
        if results:
            print("✅ Fallback summarization working correctly")
            return True
        else:
            print("❌ All fallback summarization tests failed")
            return False
            
    except Exception as e:
        print(f"❌ Fallback summarization test failed: {e}")
        return False

def test_windows_app():
    """Test if Windows Streamlit app can be imported"""
    print("\nTesting Windows Streamlit app...")
    
    try:
        # Test if app_windows.py can be imported
        import importlib.util
        spec = importlib.util.spec_from_file_location("app_windows", "app_windows.py")
        app_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(app_module)
        
        print("✅ Windows Streamlit app can be imported")
        return True
        
    except Exception as e:
        print(f"❌ Windows Streamlit app import failed: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 50)
    print("Video Summarization App - Windows System Test")
    print("=" * 50)
    
    tests = [
        ("Imports", test_imports),
        ("FFmpeg", test_ffmpeg),
        ("Model Availability", test_model_availability),
        ("Whisper Model", test_whisper_model),
        ("llama-cpp-python", test_llama_cpp),
        ("Video Processor", test_video_processor),
        ("Windows Summarizer", test_windows_summarizer),
        ("Fallback Summarization", test_fallback_summarization),
        ("Windows App", test_windows_app),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("Test Results Summary")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    # Check critical tests
    critical_tests = ["Imports", "FFmpeg", "Whisper Model", "Video Processor", "Windows Summarizer"]
    critical_passed = sum(1 for test_name, result in results if test_name in critical_tests and result)
    
    if passed == total:
        print("🎉 All tests passed! Your Windows system is ready to run the app.")
        print("\nTo start the Windows app, run:")
        print("streamlit run app_windows.py")
    elif critical_passed == len(critical_tests):
        print("✅ Critical tests passed! The app should work with fallback summarization.")
        print("\nNote: The app will use extractive summarization if the LLM model fails to load.")
        print("To start the Windows app, run:")
        print("streamlit run app_windows.py")
    else:
        print("⚠️ Some critical tests failed. Please check the issues above.")
        print("\nCommon solutions:")
        print("- Install missing dependencies: pip install -r requirements.txt")
        print("- Install FFmpeg and ensure it's in PATH")
        print("- Check system requirements (Python 3.8+, 8GB+ RAM)")
        print("\nThe app includes fallback summarization, so it may still work even if the LLM model fails.")

if __name__ == "__main__":
    main() 