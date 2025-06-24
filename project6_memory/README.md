# Bedrock Memory Chatbot

A Streamlit chatbot app using AWS Bedrock Llama 3 with local memory.

## Features
- Chat with Llama 3 via AWS Bedrock
- Local conversation memory (session-based)
- Simple Streamlit interface

## Setup

1. **Clone the repository** (if needed) and navigate to this folder.
2. **Run the setup script (Windows):**
   ```
   setup.bat
   ```
   Or manually:
   ```
   python -m venv venv
   venv\Scripts\activate
   pip install --upgrade pip
   pip install -r requirements.txt
   streamlit run app.py
   ```

## AWS Credentials
- You must have AWS credentials configured with access to Bedrock and the Llama 3 model.
- Set credentials via environment variables, `~/.aws/credentials`, or other supported methods.

## Usage
- Enter your message in the input box and press Send.
- The conversation history is shown above the input.
- Click "Clear Chat" to reset the memory.

## Customization
- Edit `app.py` to change memory behavior, prompt formatting, or UI.

## License
MIT 