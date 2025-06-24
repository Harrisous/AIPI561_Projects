# Quick Start Guide - AWS Bedrock Food Instruction Generator

This guide will help you get the AWS Bedrock Food Instruction Generator up and running in minutes.

## Prerequisites Checklist

Before starting, ensure you have:

- [ ] AWS account with Bedrock access
- [ ] Python 3.8+ installed
- [ ] AWS CLI installed and configured
- [ ] Access to Llama 3.2 90B Instruct model

## Step 1: AWS Setup

### 1.1 Configure AWS Credentials
```bash
aws configure
```
Enter your:
- AWS Access Key ID
- AWS Secret Access Key
- Default region (e.g., us-east-1)
- Default output format (json)

### 1.2 Request Model Access
1. Go to [AWS Bedrock Console](https://console.aws.amazon.com/bedrock/)
2. Navigate to "Model access"
3. Request access to `meta.llama3-2-90b-instruct-v1:0`
4. Wait for approval (usually quick)

## Step 2: Project Setup

### Option A: Automated Setup (Recommended)
```bash
# Windows
setup.bat

# macOS/Linux
chmod +x setup.sh
./setup.sh

# Cross-platform
python setup.py
```

### Option B: Manual Setup
```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Step 3: Run the Application

```bash
# Activate virtual environment (if not already active)
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# Run the app
streamlit run app.py
```

The application will open at `http://localhost:8501`

## Step 4: Test the Application

1. **Upload an Image**: Click "Browse files" and select a food photo
2. **Generate Instructions**: Click "Generate Instructions"
3. **View Results**: See detailed cooking instructions

## Troubleshooting

### Common Issues

**"NoCredentialsError"**
```bash
aws configure
```

**"AccessDeniedException"**
- Check model access in AWS Bedrock console
- Verify IAM permissions

**"ModelTimeoutException"**
- Try again in a few minutes
- Check AWS service status

**"ValidationException"**
- Check image format (JPEG, PNG supported)
- Ensure image size is reasonable (< 10MB)

**Setup Script Fails**
- Ensure Python 3.8+ is installed
- Check internet connection
- Try manual setup

### Getting Help

- **AWS Bedrock**: [Documentation](https://docs.aws.amazon.com/bedrock/)
- **Model Access**: AWS Bedrock Console
- **Application Issues**: Check README.md

## Cost Information

**Estimated costs per request:**
- Small image analysis: ~$0.01-0.05
- Large image with detailed response: ~$0.05-0.20

**Pricing:**
- Input tokens: $0.0006 per 1K tokens
- Output tokens: $0.0024 per 1K tokens
- Images: $0.0025 per image

## Next Steps

After getting the basic app running:

1. **Customize the prompt** in `app.py` for different use cases
2. **Add error handling** for production use
3. **Implement caching** to reduce costs
4. **Add authentication** for multi-user access
5. **Deploy to AWS** using Streamlit Cloud or EC2

## Security Notes

- Never commit AWS credentials to version control
- Use IAM roles when possible
- Set up billing alerts
- Monitor usage through CloudWatch 