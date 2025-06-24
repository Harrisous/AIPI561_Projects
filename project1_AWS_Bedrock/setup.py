#!/usr/bin/env python3
"""
Setup script for AWS Bedrock Food Instruction Generator
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def run_command(command, check=True):
    """Run a command and return the result."""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if check and result.returncode != 0:
            print(f"ERROR: Command failed: {command}")
            print(f"Error: {result.stderr}")
            return False
        return result.returncode == 0
    except Exception as e:
        print(f"ERROR: Failed to run command '{command}': {e}")
        return False

def check_python():
    """Check if Python is installed and has the right version."""
    print("Checking Python installation...")
    
    if sys.version_info < (3, 8):
        print("ERROR: Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    
    print(f"Python {sys.version.split()[0]} found!")
    return True

def check_aws_cli():
    """Check if AWS CLI is installed and configured."""
    print("\nChecking AWS CLI installation...")
    
    if not run_command("aws --version", check=False):
        print("WARNING: AWS CLI is not installed")
        print("Please install AWS CLI:")
        if platform.system() == "Darwin":  # macOS
            print("  brew install awscli")
        elif platform.system() == "Linux":
            print("  sudo apt-get install awscli")
        else:  # Windows
            print("  Download from https://aws.amazon.com/cli/")
        print("\nAfter installation, run: aws configure")
        input("\nPress Enter to continue...")
        return False
    
    print("AWS CLI found!")
    
    print("Checking AWS credentials...")
    if not run_command("aws sts get-caller-identity", check=False):
        print("WARNING: AWS credentials not configured")
        print("Please run: aws configure")
        input("\nPress Enter to continue...")
        return False
    
    print("AWS credentials configured!")
    return True

def create_virtual_environment():
    """Create a virtual environment."""
    print("\nCreating virtual environment...")
    
    if os.path.exists(".venv"):
        print("Virtual environment already exists")
        return True
    
    if not run_command(f"{sys.executable} -m venv .venv"):
        return False
    
    print("Virtual environment created!")
    return True

def install_dependencies():
    """Install Python dependencies."""
    print("Installing dependencies...")
    
    # Determine the pip command based on the platform
    if platform.system() == "Windows":
        pip_cmd = ".venv\\Scripts\\pip"
    else:
        pip_cmd = ".venv/bin/pip"
    
    if not run_command(f"{pip_cmd} install -r requirements.txt"):
        return False
    
    print("Dependencies installed!")
    return True

def main():
    """Main setup function."""
    print("=" * 50)
    print("AWS Bedrock Food Instruction Generator")
    print("=" * 50)
    print()
    
    # Check Python
    if not check_python():
        sys.exit(1)
    
    # Check AWS CLI
    check_aws_cli()
    
    # Create virtual environment
    if not create_virtual_environment():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        sys.exit(1)
    
    print("\n" + "=" * 50)
    print("Setup completed successfully!")
    print("=" * 50)
    print()
    print("Next steps:")
    print("1. Ensure you have AWS Bedrock access")
    print("2. Request access to meta.llama3.2-11b-vision-instruct-v1:0")
    print("3. Activate the virtual environment:")
    if platform.system() == "Windows":
        print("   .venv\\Scripts\\activate")
    else:
        print("   source .venv/bin/activate")
    print("4. Run: streamlit run app.py")
    print()
    print("For more information, see README.md")
    print()

if __name__ == "__main__":
    main() 