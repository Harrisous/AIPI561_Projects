#!/bin/bash

echo "🚀 Food Instruction Generator Setup"
echo "===================================="

# Check if Python is installed
echo ""
echo "📦 Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 is not installed"
    echo "Please install Python3 first"
    exit 1
fi
echo "✅ Python3 is installed"

# Install Python dependencies
echo ""
echo "📦 Installing Python dependencies..."
pip3 install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "❌ Failed to install Python dependencies"
    exit 1
fi
echo "✅ Python dependencies installed"

# Check if Ollama is installed
echo ""
echo "📦 Checking Ollama installation..."
if ! command -v ollama &> /dev/null; then
    echo "❌ Ollama is not installed"
    echo "Installing Ollama..."
    
    # Detect OS and install accordingly
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        if command -v brew &> /dev/null; then
            brew install ollama
        else
            echo "❌ Homebrew not found. Please install Homebrew first or download from https://ollama.ai/download"
            exit 1
        fi
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        curl -fsSL https://ollama.ai/install.sh | sh
    else
        echo "❌ Unsupported operating system"
        echo "Please install Ollama manually from https://ollama.ai/download"
        exit 1
    fi
    
    if [ $? -ne 0 ]; then
        echo "❌ Failed to install Ollama"
        exit 1
    fi
    echo "✅ Ollama installed successfully"
else
    echo "✅ Ollama is already installed"
fi

# Start Ollama service
echo ""
echo "🚀 Starting Ollama service..."
ollama serve &
OLLAMA_PID=$!
sleep 5

# Check if Ollama is running
if ! curl -s http://localhost:11434/api/tags > /dev/null; then
    echo "❌ Failed to start Ollama service"
    exit 1
fi
echo "✅ Ollama service is running"

# Pull the model
echo ""
echo "📥 Pulling Llama 3.2 11B Vision Instruct model..."
echo "This may take several minutes depending on your internet connection..."
ollama pull llama3.2-11b-vision-instruct
if [ $? -ne 0 ]; then
    echo "❌ Failed to pull the model"
    exit 1
fi
echo "✅ Model pulled successfully"

echo ""
echo "🎉 Setup completed successfully!"
echo ""
echo "📋 To run the application:"
echo "1. Make sure Ollama is running: ollama serve"
echo "2. Run: streamlit run app.py"
echo "3. Open your browser to http://localhost:8501"
echo "" 