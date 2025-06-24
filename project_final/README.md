# URL Sentiment Analyzer with Bedrock Llama 3.2

## Overview
This project is a Streamlit web application that analyzes the market sentiment impact of news articles or web content. By entering a URL, the app fetches the page content, then uses Amazon Bedrock's Llama 3.2 90B Vision Instruct model to classify the sentiment and identify affected financial assets.

## Features
- Fetches and extracts visible text from any public URL
- Analyzes sentiment with Bedrock Llama 3.2 90B Vision Instruct
- Classifies sentiment as Strong Positive, Moderate Positive, Neutral, Moderate Negative, or Strong Negative
- Identifies affected assets/companies and provides concise reasoning
- Visualizes sentiment with progress bars and icons

## Setup Instructions
1. **Clone the repository** (if not already):
   ```bash
   git clone <repo-url>
   cd <repo-directory>/AIPI561_Projects/project_final
   ```
2. **Create and activate a virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On Mac/Linux:
   source venv/bin/activate
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Configure AWS credentials:**
   - Ensure you have AWS credentials with access to Bedrock in `us-east-2` region.
   - Set up your credentials using `aws configure` or environment variables.

## Usage
1. **Run the Streamlit app:**
   ```bash
   streamlit run app.py
   ```
2. **In your browser:**
   - Enter a news article or web page URL.
   - View the extracted content and sentiment analysis results.

## Requirements
- Python 3.8+
- Streamlit
- boto3
- requests
- beautifulsoup4

Install all requirements with:
```bash
pip install -r requirements.txt
```

## Troubleshooting
- **Error fetching content:** Some sites may block automated access. Try a different URL.
- **AWS errors:** Ensure your credentials are correct and have Bedrock access in `us-east-2`.
- **Model errors:** If the model returns no output, check your AWS quota and model permissions.

## License
See [LICENSE](LICENSE) for details. 