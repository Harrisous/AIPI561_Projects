#!/usr/bin/env python3
"""
Setup script for Food Instruction Generator with Ollama
"""

import subprocess
import sys
import os
import platform
import requests
import time

def run_command(command, description):
    """Run a command and handle errors."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e.stderr}")
        return False

def check_ollama_installed():
    """Check if Ollama is installed."""
    try:
        result = subprocess.run(["ollama", "--version"], capture_output=True, text=True)
        return result.returncode == 0
    except FileNotFoundError:
        return False

def install_ollama():
    """Install Ollama based on the operating system."""
    system = platform.system().lower()
    
    if system == "windows":
        print("🔄 Installing Ollama on Windows...")
        # Try winget first
        if run_command("winget install Ollama.Ollama", "Installing Ollama via winget"):
            return True
        else:
            print("📥 Please download and install Ollama manually from https://ollama.ai/download")
            return False
    
    elif system == "darwin":  # macOS
        if run_command("brew install ollama", "Installing Ollama via Homebrew"):
            return True
        else:
            print("📥 Please install Homebrew first or download from https://ollama.ai/download")
            return False
    
    elif system == "linux":
        if run_command("curl -fsSL https://ollama.ai/install.sh | sh", "Installing Ollama on Linux"):
            return True
        else:
            print("❌ Failed to install Ollama on Linux")
            return False
    
    else:
        print(f"❌ Unsupported operating system: {system}")
        return False

def install_python_dependencies():
    """Install Python dependencies."""
    return run_command("pip install -r requirements.txt", "Installing Python dependencies")

def start_ollama_service():
    """Start the Ollama service."""
    print("🔄 Starting Ollama service...")
    try:
        # Start Ollama in the background
        subprocess.Popen(["ollama", "serve"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(3)  # Wait for service to start
        
        # Check if service is running
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            print("✅ Ollama service is running")
            return True
        else:
            print("❌ Ollama service failed to start")
            return False
    except Exception as e:
        print(f"❌ Failed to start Ollama service: {e}")
        return False

def pull_model(model_name="llama3.2-11b-vision-instruct"):
    """Pull the specified model."""
    print(f"🔄 Pulling {model_name} model (this may take a while)...")
    return run_command(f"ollama pull {model_name}", f"Pulling {model_name} model")

def main():
    print("🚀 Setting up Food Instruction Generator with Ollama")
    print("=" * 50)
    
    # Check if Ollama is installed
    if not check_ollama_installed():
        print("📦 Ollama is not installed. Installing now...")
        if not install_ollama():
            print("❌ Failed to install Ollama. Please install manually.")
            return False
    else:
        print("✅ Ollama is already installed")
    
    # Install Python dependencies
    if not install_python_dependencies():
        print("❌ Failed to install Python dependencies")
        return False
    
    # Start Ollama service
    if not start_ollama_service():
        print("❌ Failed to start Ollama service")
        return False
    
    # Pull the model
    if not pull_model():
        print("❌ Failed to pull the model")
        return False
    
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Make sure Ollama is running: ollama serve")
    print("2. Run the Streamlit app: streamlit run app.py")
    print("3. Open your browser to http://localhost:8501")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 