# Duke University Q&A Agent

A Streamlit-based AI agent that answers questions specifically about Duke University. It uses Tavily for web search restricted to Duke domains and AWS Bedrock's Llama 3 model for generating answers.

## Features
- Answers questions only about Duke University
- Uses Tavily API to search Duke-related web content
- Uses AWS Bedrock (Llama 3) for generating expert answers
- Simple Streamlit web interface

## Setup Instructions

### 1. Clone the repository
```
git clone <repo-url>
cd project5_agent
```

### 2. Set up a virtual environment (Windows)
```
setup.bat
```
This will create a virtual environment, activate it, and install all dependencies.

### 3. Set Environment Variables
Create a `.env` file in the project directory with the following content:
```
TAVILY_API_KEY=your_tavily_api_key
```
- Get your Tavily API key from [Tavily](https://www.tavily.com/)
- Set up AWS credentials for Bedrock access ([AWS docs](https://docs.aws.amazon.com/bedrock/latest/userguide/setting-up.html))

## Usage
Activate the virtual environment if not already active:
```
venv\Scripts\activate
```
Then run the Streamlit app:
```
streamlit run app.py
```
Open the provided local URL in your browser. Enter your Duke-related question in the input box.

## Dependencies
- streamlit
- boto3
- tavily-python
- dotenv

All dependencies are listed in `requirements.txt`.

## How it works
- The app checks if your question is about Duke University.
- If yes, it uses Tavily to search for relevant Duke web content.
- The search results are provided as context to the Llama 3 model via AWS Bedrock.
- The model generates an answer, which is displayed in the app.
- If the question is not about Duke, the app will not answer.

## License
See LICENSE file for details.
