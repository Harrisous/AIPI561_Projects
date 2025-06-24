"""
Video Summarization App - Streamlit Interface (Windows Version)
Uses llama-cpp-python for GGUF model inference
"""

import streamlit as st
import os
import tempfile
import time
from pathlib import Path
import logging

# Import our modules (Windows version)
from config import UI_CONFIG, validate_config, get_model_path
from video_processor import VideoProcessor, check_ffmpeg_availability
from summarizer_windows import TextSummarizer, get_available_summary_styles

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title=UI_CONFIG["page_title"] + " (Windows)",
    page_icon=UI_CONFIG["page_icon"],
    layout=UI_CONFIG["layout"],
    initial_sidebar_state=UI_CONFIG["initial_sidebar_state"]
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 2rem;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .info-box {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #d4edda;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #28a745;
        margin: 1rem 0;
    }
    .error-box {
        background-color: #f8d7da;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #dc3545;
        margin: 1rem 0;
    }
    .metric-card {
        background-color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 0.5rem 0;
    }
    .windows-info {
        background-color: #e3f2fd;
        padding: 0.5rem;
        border-radius: 0.25rem;
        border-left: 3px solid #2196f3;
        margin: 0.5rem 0;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables"""
    if 'video_processed' not in st.session_state:
        st.session_state.video_processed = False
    if 'transcription' not in st.session_state:
        st.session_state.transcription = ""
    if 'summary' not in st.session_state:
        st.session_state.summary = ""
    if 'video_info' not in st.session_state:
        st.session_state.video_info = None
    if 'processing_error' not in st.session_state:
        st.session_state.processing_error = None

def check_system_requirements():
    """Check if all system requirements are met"""
    issues = validate_config()
    
    if issues:
        st.error("⚠️ System Requirements Issues:")
        for issue in issues:
            st.error(f"• {issue}")
        return False
    
    st.success("✅ All system requirements met!")
    return True

def sidebar_configuration():
    """Sidebar configuration options"""
    st.sidebar.title("⚙️ Configuration")
    
    # Windows info
    st.sidebar.markdown('<div class="windows-info">🪟 Windows-compatible version</div>', unsafe_allow_html=True)
    st.sidebar.markdown('<div class="windows-info">🤖 Using llama-cpp-python (GGUF backend)</div>', unsafe_allow_html=True)
    
    # Model selection
    st.sidebar.subheader("Model Settings")
    model_path = get_model_path()
    if model_path:
        st.sidebar.success(f"Model: {Path(model_path).name}")
    else:
        st.sidebar.error("No GGUF model found")
    
    # Summary settings
    st.sidebar.subheader("Summary Settings")
    summary_style = st.sidebar.selectbox(
        "Summary Style",
        get_available_summary_styles(),
        index=0
    )
    
    max_length = st.sidebar.slider(
        "Maximum Summary Length (words)",
        min_value=50,
        max_value=1000,
        value=500,
        step=50
    )
    
    # Whisper model selection
    st.sidebar.subheader("Speech Recognition")
    whisper_model = st.sidebar.selectbox(
        "Whisper Model Size",
        ["tiny", "base", "small", "medium", "large"],
        index=1,
        help="Larger models are more accurate but slower"
    )
    
    return {
        "summary_style": summary_style,
        "max_length": max_length,
        "whisper_model": whisper_model
    }

def main_header():
    """Display main header"""
    st.markdown('<h1 class="main-header">🎥 Video Summarization</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Transform videos into concise summaries using AI (Windows Version)</p>', unsafe_allow_html=True)
    
    # Windows compatibility info
    st.info("🪟 **Windows-Compatible Version**: This version uses **llama-cpp-python** for GGUF model inference. No C++ build tools required!")

def upload_section():
    """Video upload section"""
    st.header("📁 Upload Video")
    
    uploaded_file = st.file_uploader(
        "Choose a video file",
        type=['mp4', 'avi', 'mov', 'mkv', 'wmv', 'flv', 'webm'],
        help="Supported formats: MP4, AVI, MOV, MKV, WMV, FLV, WEBM"
    )
    
    if uploaded_file is not None:
        # Display file info
        file_details = {
            "Filename": uploaded_file.name,
            "File size": f"{uploaded_file.size / (1024*1024):.2f} MB",
            "File type": uploaded_file.type
        }
        
        st.write("**File Details:**")
        for key, value in file_details.items():
            st.write(f"• {key}: {value}")
        
        return uploaded_file
    
    return None

def process_video_section(uploaded_file):
    """Video processing section"""
    st.header("🔄 Process Video")
    
    if st.button("🚀 Process Video", type="primary", use_container_width=True):
        if uploaded_file is None:
            st.error("Please upload a video file first")
            return
        
        with st.spinner("Processing video..."):
            try:
                # Save uploaded file temporarily
                with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp_file:
                    tmp_file.write(uploaded_file.getvalue())
                    temp_video_path = tmp_file.name
                
                # Initialize video processor
                video_processor = VideoProcessor()
                
                # Process video
                result = video_processor.process_video(temp_video_path)
                
                # Clean up temporary file
                os.unlink(temp_video_path)
                
                if result["success"]:
                    st.session_state.video_processed = True
                    st.session_state.transcription = result["transcription"]
                    st.session_state.video_info = result["video_info"]
                    st.session_state.processing_error = None
                    
                    st.success("✅ Video processed successfully!")
                    
                    # Display video info
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Duration", f"{result['video_info']['duration']:.1f}s" if result['video_info']['duration'] else "Unknown")
                    with col2:
                        st.metric("Words", result["word_count"])
                    with col3:
                        st.metric("Characters", len(result["transcription"]))
                    
                    # Show transcription preview
                    with st.expander("📝 View Transcription"):
                        st.text_area("Transcription", result["transcription"], height=200)
                    
                else:
                    st.session_state.processing_error = result["error"]
                    st.error(f"❌ Processing failed: {result['error']}")
                    
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                logger.error(f"Video processing error: {e}")

def summarize_section():
    """Text summarization section"""
    st.header("📝 Generate Summary")
    
    if not st.session_state.video_processed:
        st.info("Please process a video first to generate a summary")
        return
    
    if st.session_state.processing_error:
        st.error(f"Cannot generate summary due to processing error: {st.session_state.processing_error}")
        return
    
    config = sidebar_configuration()
    
    if st.button("🧠 Generate Summary", type="primary", use_container_width=True):
        with st.spinner("Generating summary..."):
            try:
                # Initialize summarizer (Windows version)
                summarizer = TextSummarizer()
                
                # Generate summary
                result = summarizer.summarize_text(
                    st.session_state.transcription,
                    style=config["summary_style"],
                    max_length=config["max_length"]
                )
                
                if result["success"]:
                    st.session_state.summary = result["summary"]
                    
                    st.success("✅ Summary generated successfully!")
                    
                    # Display summary metrics
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Summary Words", result["word_count"])
                    with col2:
                        st.metric("Processing Time", f"{result['processing_time']:.2f}s")
                    with col3:
                        compression_ratio = result["word_count"] / len(st.session_state.transcription.split())
                        st.metric("Compression Ratio", f"{compression_ratio:.1%}")
                    
                    # Display summary
                    st.subheader("📋 Generated Summary")
                    st.markdown(f"**Style:** {result['style'].title()}")
                    st.text_area("Summary", result["summary"], height=300)
                    
                else:
                    st.error(f"❌ Summary generation failed: {result['error']}")
                    
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                logger.error(f"Summary generation error: {e}")

def download_section():
    """Download results section"""
    st.header("💾 Download Results")
    
    if not st.session_state.summary:
        st.info("Generate a summary first to download results")
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Download summary
        summary_data = st.session_state.summary.encode()
        st.download_button(
            label="📄 Download Summary",
            data=summary_data,
            file_name="video_summary.txt",
            mime="text/plain",
            use_container_width=True
        )
    
    with col2:
        # Download transcription
        transcription_data = st.session_state.transcription.encode()
        st.download_button(
            label="📝 Download Transcription",
            data=transcription_data,
            file_name="video_transcription.txt",
            mime="text/plain",
            use_container_width=True
        )

def model_info_section():
    """Display model information"""
    st.sidebar.header("🤖 Model Information")
    
    try:
        summarizer = TextSummarizer()
        model_info = summarizer.get_model_info()
        
        if "error" not in model_info:
            st.sidebar.write(f"**Model:** {model_info['model_name']}")
            st.sidebar.write(f"**Size:** {model_info['model_size_mb']:.1f} MB")
            st.sidebar.write(f"**Context:** {model_info['context_size']}")
            st.sidebar.write(f"**Threads:** {model_info['threads']}")
            st.sidebar.write(f"**Backend:** {model_info['backend']}")
            
            # Test model
            if st.sidebar.button("🧪 Test Model"):
                with st.sidebar.spinner("Testing..."):
                    test_result = summarizer.test_model()
                    if test_result["success"]:
                        st.sidebar.success("✅ Model working!")
                    else:
                        st.sidebar.error("❌ Model test failed")
        else:
            st.sidebar.error(f"Model error: {model_info['error']}")
            
    except Exception as e:
        st.sidebar.error(f"Error loading model: {e}")

def main():
    """Main application function"""
    # Initialize session state
    initialize_session_state()
    
    # Display header
    main_header()
    
    # Check system requirements
    if not check_system_requirements():
        st.stop()
    
    # Sidebar configuration
    model_info_section()
    
    # Main content
    uploaded_file = upload_section()
    
    if uploaded_file:
        process_video_section(uploaded_file)
        summarize_section()
        download_section()
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666;'>
            <p>Built with ❤️ using Streamlit, Hugging Face, and llama-cpp-python</p>
            <p>Video Summarization App v1.0 (Windows Version)</p>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main() 