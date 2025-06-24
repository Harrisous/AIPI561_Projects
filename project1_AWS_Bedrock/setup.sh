#!/bin/bash

echo "========================================"
echo "AWS Bedrock Food Instruction Generator"
echo "========================================"
echo

# Check Python installation
echo "Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed or not in PATH"
    echo "Please install Python 3 from https://python.org"
    exit 1
fi

echo "Python found!"
echo

# Check AWS CLI installation
echo "Checking AWS CLI installation..."
if ! command -v aws &> /dev/null; then
    echo "WARNING: AWS CLI is not installed"
    echo "Please install AWS CLI:"
    echo "  macOS: brew install awscli"
    echo "  Linux: sudo apt-get install awscli"
    echo "  Or download from https://aws.amazon.com/cli/"
    echo
    echo "After installation, run: aws configure"
    echo
    read -p "Press Enter to continue..."
else
    echo "AWS CLI found!"
    echo
    
    echo "Checking AWS credentials..."
    if aws sts get-caller-identity &> /dev/null; then
        echo "AWS credentials configured!"
    else
        echo "WARNING: AWS credentials not configured"
        echo "Please run: aws configure"
        echo
        read -p "Press Enter to continue..."
    fi
fi

echo
echo "Creating virtual environment..."
python3 -m venv .venv
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to create virtual environment"
    exit 1
fi

echo "Activating virtual environment..."
source .venv/bin/activate

echo "Installing dependencies..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    exit 1
fi

echo
echo "========================================"
echo "Setup completed successfully!"
echo "========================================"
echo
echo "Next steps:"
echo "1. Ensure you have AWS Bedrock access"
echo "2. Request access to meta.llama3.2-11b-vision-instruct-v1:0"
echo "3. Run: streamlit run app.py"
echo
echo "For more information, see README.md"
echo 