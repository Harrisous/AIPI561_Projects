# Food Instruction Generator with AWS Bedrock and Streamlit

This project uses Meta's Llama 3.2 90B Instruct model hosted on AWS Bedrock to provide cooking instructions based on uploaded food photos.

## Prerequisites

### 1. AWS Account and Bedrock Access

**AWS Account Setup:**
- Create an AWS account if you don't have one
- Ensure you have access to AWS Bedrock service
- Request access to the Llama 3.2 90B Instruct model in the AWS Bedrock console

**Bedrock Model Access:**
1. Go to the [AWS Bedrock Console](https://console.aws.amazon.com/bedrock/)
2. Navigate to "Model access" in the left sidebar
3. Request access to "meta.llama3-2-90b-instruct-v1:0"
4. Wait for approval (usually takes a few minutes to hours)

### 2. AWS Credentials Configuration

**Option 1: AWS CLI (Recommended)**
```bash
# Install AWS CLI
# Windows: Download from https://aws.amazon.com/cli/
# macOS: brew install awscli
# Linux: sudo apt-get install awscli

# Configure AWS credentials
aws configure
```

**Option 2: Environment Variables**
```bash
# Set environment variables
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key
export AWS_DEFAULT_REGION=us-east-1
```

**Option 3: IAM Role (for EC2/ECS)**
- Attach an IAM role with Bedrock permissions to your instance

### 3. Required IAM Permissions

Your AWS user/role needs the following permissions:
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "bedrock:InvokeModel",
                "bedrock:ListFoundationModels"
            ],
            "Resource": "*"
        }
    ]
}
```

### 4. Install Python Dependencies

```bash
pip install -r requirements.txt
```

## Usage

### 1. Run the Streamlit Application

```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`.

### 2. Using the Application

1. **Upload an Image**: Click "Browse files" to upload a food photo
2. **Generate Instructions**: Click "Generate Instructions" to analyze the image
3. **View Results**: The app will display detailed cooking instructions

## Features

- Upload food photos through a user-friendly interface
- Get detailed cooking instructions and recipe suggestions
- Real-time processing with the Llama 3.2 90B Instruct model on AWS Bedrock
- Vision capabilities for image analysis
- Responsive design for various screen sizes
- AWS region selection for optimal performance

## Troubleshooting

### AWS Credentials Issues
```bash
# Check if credentials are configured
aws sts get-caller-identity

# Reconfigure if needed
aws configure
```

### Bedrock Access Issues
- **"Access Denied"**: Ensure you have requested and received model access
- **"Model not found"**: Check if the model is available in your selected region
- **"Service not available"**: Verify Bedrock is available in your AWS region

### Common Error Messages

**"NoCredentialsError"**
```bash
# Configure AWS credentials
aws configure
```

**"AccessDeniedException"**
- Request model access in AWS Bedrock console
- Check IAM permissions

**"ModelTimeoutException"**
- The model may be experiencing high load
- Try again in a few minutes

**"ValidationException"**
- Check image format (JPEG, PNG supported)
- Ensure image size is reasonable (< 10MB)

## Cost Considerations

AWS Bedrock pricing for Llama 3.2 90B Instruct:
- **Input tokens**: $0.0006 per 1K tokens
- **Output tokens**: $0.0024 per 1K tokens
- **Images**: $0.0025 per image

**Estimated costs per request:**
- Small image analysis: ~$0.01-0.05
- Large image with detailed response: ~$0.05-0.20

## Project Structure

```
project1_AWS_Bedrock/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── setup.bat          # Windows setup script
├── setup.sh           # Unix setup script
├── setup.py           # Cross-platform setup script
├── QUICK_START.md     # Quick start guide
└── README.md          # This file
```

## Security Best Practices

1. **Never commit AWS credentials** to version control
2. **Use IAM roles** when possible instead of access keys
3. **Limit permissions** to only what's necessary
4. **Monitor usage** through AWS CloudWatch
5. **Set up billing alerts** to avoid unexpected charges

## Support

For issues related to:
- **AWS Bedrock**: Check the [AWS Bedrock documentation](https://docs.aws.amazon.com/bedrock/)
- **Model access**: Contact AWS support through the console
- **Application issues**: Check the troubleshooting section above
