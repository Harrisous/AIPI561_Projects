import streamlit as st
import requests
import base64
import io
from PIL import Image
import json
import time
from typing import Optional

# Page configuration
st.set_page_config(
    page_title="Food Instruction Generator",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #FF6B6B;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .sub-header {
        font-size: 1.5rem;
        text-align: center;
        color: #4ECDC4;
        margin-bottom: 2rem;
    }
    .upload-section {
        background-color: #f8f9fa;
        padding: 2rem;
        border-radius: 10px;
        border: 2px dashed #dee2e6;
        text-align: center;
        margin: 2rem 0;
    }
    .result-section {
        background-color: #e8f5e8;
        padding: 2rem;
        border-radius: 10px;
        border-left: 5px solid #28a745;
        margin: 2rem 0;
    }
    .error-section {
        background-color: #f8d7da;
        padding: 2rem;
        border-radius: 10px;
        border-left: 5px solid #dc3545;
        margin: 2rem 0;
    }
    .stButton > button {
        background-color: #FF6B6B;
        color: white;
        border-radius: 25px;
        padding: 0.5rem 2rem;
        font-weight: bold;
        border: none;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        background-color: #FF5252;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
</style>
""", unsafe_allow_html=True)

def check_ollama_connection() -> bool:
    """Check if Ollama is running and accessible."""
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

def check_model_availability(model_name: str) -> bool:
    """Check if the specified model is available in Ollama."""
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json().get("models", [])
            return any(model["name"] == model_name for model in models)
        return False
    except requests.exceptions.RequestException:
        return False

def encode_image_to_base64(image: Image.Image) -> str:
    """Convert PIL Image to base64 string."""
    buffer = io.BytesIO()
    
    # Convert RGBA to RGB if necessary (JPEG doesn't support alpha channel)
    if image.mode == 'RGBA':
        # Create a white background
        rgb_image = Image.new('RGB', image.size, (255, 255, 255))
        rgb_image.paste(image, mask=image.split()[-1])  # Use alpha channel as mask
        image = rgb_image
    elif image.mode != 'RGB':
        # Convert other modes to RGB
        image = image.convert('RGB')
    
    image.save(buffer, format="JPEG")
    img_str = base64.b64encode(buffer.getvalue()).decode()
    return img_str

def generate_food_instructions(image: Image.Image, model_name: str = "llama3.2-vision:11b") -> Optional[str]:
    """Generate food instructions using Ollama API."""
    
    # Prepare the image
    img_base64 = encode_image_to_base64(image)
    
    # Prepare the prompt
    prompt = """You are a helpful cooking assistant. Analyze this food image and provide detailed cooking instructions, including:
1. What dish this appears to be
2. Estimated cooking time
3. Step-by-step cooking instructions
4. Key ingredients that might be needed
5. Cooking tips and techniques
6. Serving suggestions

Please provide clear, practical instructions that a home cook can follow easily."""

    # Prepare the request payload
    payload = {
        "model": model_name,
        "prompt": prompt,
        "images": [img_base64],
        "stream": False,
        "options": {
            "temperature": 0.7,
            "top_p": 0.9,
            "max_tokens": 1000
        }
    }

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json=payload,
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            return result.get("response", "No response generated")
        else:
            st.error(f"Error from Ollama API: {response.status_code}")
            return None
            
    except requests.exceptions.RequestException as e:
        st.error(f"Connection error: {str(e)}")
        return None
    except Exception as e:
        st.error(f"Unexpected error: {str(e)}")
        return None

def main():
    # Header
    st.markdown('<h1 class="main-header">🍽️ Food Instruction Generator</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Upload a photo of your food and get detailed cooking instructions!</p>', unsafe_allow_html=True)
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Check Ollama connection
        if check_ollama_connection():
            st.success("✅ Ollama is running")
        else:
            st.error("❌ Ollama is not running")
            st.info("Please start Ollama with: `ollama serve`")
            return
        
        # Model selection
        model_name = st.selectbox(
            "Select Model",
            ["llama3.2-vision:11b"],
            help="Choose the vision model to use for analysis"
        )
        
        # Check model availability
        if check_model_availability(model_name):
            st.success(f"✅ {model_name} is available")
        else:
            st.error(f"❌ {model_name} is not available")
            st.info(f"Please pull the model with: `ollama pull {model_name}`")
            return
        
        # Additional options
        st.header("ℹ️ About")
        st.info("""
        This app uses Meta's Llama 3.2 Vision model to analyze food photos and provide cooking instructions.
        
        **Features:**
        - Image analysis
        - Recipe suggestions
        - Cooking instructions
        - Ingredient recommendations
        """)
    
    # Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown('<div class="upload-section">', unsafe_allow_html=True)
        st.header("📸 Upload Food Photo")
        
        uploaded_file = st.file_uploader(
            "Choose an image file",
            type=['png', 'jpg', 'jpeg'],
            help="Upload a clear photo of the food you want cooking instructions for"
        )
        
        if uploaded_file is not None:
            # Display the uploaded image
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", use_column_width=True)
            
            # Generate button
            if st.button("🍳 Generate Instructions", type="primary"):
                with st.spinner("Analyzing your food and generating instructions..."):
                    instructions = generate_food_instructions(image, model_name)
                    
                    if instructions:
                        st.markdown('</div>', unsafe_allow_html=True)
                        st.markdown('<div class="result-section">', unsafe_allow_html=True)
                        st.header("📝 Cooking Instructions")
                        st.markdown(instructions)
                        st.markdown('</div>', unsafe_allow_html=True)
                    else:
                        st.markdown('</div>', unsafe_allow_html=True)
                        st.markdown('<div class="error-section">', unsafe_allow_html=True)
                        st.error("Failed to generate instructions. Please try again.")
                        st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("👆 Please upload a food image to get started!")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.header("💡 Tips for Best Results")
        st.markdown("""
        **For better results:**
        
        🎯 **Take clear photos** - Good lighting and focus
        📐 **Show the full dish** - Include all components
        🍽️ **Use a clean background** - Avoid cluttered surfaces
        📱 **High resolution** - Better quality images work better
        
        **What you'll get:**
        - Dish identification
        - Cooking time estimates
        - Step-by-step instructions
        - Ingredient suggestions
        - Cooking tips
        - Serving recommendations
        """)
        
        st.header("🔧 Troubleshooting")
        st.markdown("""
        **Common issues:**
        
        ❌ **Model not found**
        ```bash
        ollama pull llama3.2-vision:11b
        ```
        
        ❌ **Ollama not running**
        ```bash
        ollama serve
        ```
        
        ❌ **Memory issues**
        - Close other applications
        - Ensure 16GB+ RAM available
        """)

if __name__ == "__main__":
    main()
