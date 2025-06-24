import streamlit as st
import boto3
import base64
import io
from PIL import Image
import json
import time
from typing import Optional
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Food Instruction Generator - AWS Bedrock",
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

def check_aws_credentials() -> bool:
    """Check if AWS credentials are properly configured."""
    try:
        # Try to create a Bedrock client
        bedrock = boto3.client('bedrock', region_name='us-east-1')
        return True
    except Exception as e:
        st.error(f"AWS credentials error: {str(e)}")
        return False

def check_bedrock_access() -> bool:
    """Check if we can access AWS Bedrock service."""
    try:
        # Use the regular bedrock client (not bedrock-runtime) for listing models
        bedrock = boto3.client('bedrock', region_name='us-east-1')
        # Try to list foundation models (this will fail if no access)
        bedrock.list_foundation_models()
        return True
    except Exception as e:
        st.error(f"Bedrock access error: {str(e)}")
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

def generate_food_instructions(image: Image.Image, model_id: str) -> Optional[str]:
    # Convert PIL Image to bytes (PNG format)
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    image_bytes = buffer.getvalue()

    user_message = (
        "You are a helpful cooking assistant. Analyze this food image and provide detailed cooking instructions, including:\n"
        "1. What dish this appears to be\n"
        "2. Estimated cooking time\n"
        "3. Step-by-step cooking instructions\n"
        "4. Key ingredients that might be needed\n"
        "5. Cooking tips and techniques\n"
        "6. Serving suggestions\n\n"
        "Please provide clear, practical instructions that a home cook can follow easily."
    )

    messages = [
        {
            "role": "user",
            "content": [
                {"image": {"format": "png", "source": {"bytes": image_bytes}}},
                {"text": user_message},
            ],
        }
    ]

    try:
        bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')
        response = bedrock.converse(
            modelId=model_id,
            messages=messages,
        )
        response_text = response["output"]["message"]["content"][0]["text"]
        return response_text
    except Exception as e:
        st.error(f"Error calling Bedrock API: {str(e)}")
        return None

def main():
    # Header
    st.markdown('<h1 class="main-header">🍽️ Food Instruction Generator</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Upload a photo of your food and get detailed cooking instructions using AWS Bedrock!</p>', unsafe_allow_html=True)
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Check AWS credentials
        if check_aws_credentials():
            st.success("✅ AWS credentials configured")
        else:
            st.error("❌ AWS credentials not configured")
            st.info("Please configure AWS credentials using AWS CLI or environment variables")
            return
        
        # Check Bedrock access
        if check_bedrock_access():
            st.success("✅ AWS Bedrock access confirmed")
        else:
            st.error("❌ Cannot access AWS Bedrock")
            st.info("Please ensure you have Bedrock access and proper permissions")
            return
        
        # Model selection
        model_id = st.selectbox(
            "Select Model",
            ["arn:aws:bedrock:us-east-1:247140043804:inference-profile/us.meta.llama3-2-90b-instruct-v1:0"],
            help="Choose the model to use for analysis"
        )
        
        # AWS Region
        aws_region = st.selectbox(
            "AWS Region",
            ["us-east-1"],
            help="Select the AWS region where Bedrock is available"
        )
        
        # Additional options
        st.header("ℹ️ About")
        st.info("""
        This app uses Meta's Llama 3.2 90B Vision Instruct model on AWS Bedrock to analyze food photos and provide cooking instructions.
        
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
                    instructions = generate_food_instructions(image, model_id)
                    
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
        
        ❌ **AWS credentials not configured**
        ```bash
        aws configure
        ```
        
        ❌ **No Bedrock access**
        - Request access in AWS Console
        - Ensure proper IAM permissions
        
        ❌ **Model not available**
        - Check if model is available in your region
        - Ensure you have model access permissions
        """)

if __name__ == "__main__":
    main()
