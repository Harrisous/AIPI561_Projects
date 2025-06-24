import streamlit as st
import requests
import boto3
import json
from urllib.parse import urlparse

# Helper to fetch text content from a URL
@st.cache_data(show_spinner=False)
def fetch_url_content(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 429:
            return "Error fetching content: 429 Too Many Requests. This site is blocking automated access. Please try a different URL."
        response.raise_for_status()
        # Try to extract text content (simple approach)
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        # Get visible text
        texts = soup.stripped_strings
        return ' '.join(texts)
    except Exception as e:
        return f"Error fetching content: {e}"

# Helper to call Bedrock Llama 3.2 90B Vision Instruct
@st.cache_data(show_spinner=False)
def analyze_sentiment_bedrock(text):
    try:
        bedrock = boto3.client('bedrock-runtime', region_name='us-east-2')
        prompt = f"""
            Analyze the market sentiment impact of the following news content.  
            **Guidelines**:  
            1. Focus on financial markets (stocks, commodities, crypto)  
            2. Consider historical context and sector-specific implications  
            3. Classify sentiment as:  
            - **Strong Positive** (e.g., mergers, breakthrough innovations)  
            - **Moderate Positive** (e.g., earnings beat, regulatory easing)  
            - **Neutral** (no clear market impact)  
            - **Moderate Negative** (e.g., supply chain disruptions)  
            - **Strong Negative** (e.g., bankruptcy, severe regulation)  
            4. Identify affected assets/companies (e.g., $AAPL, Oil futures)  
            5. Add brief reasoning (1 sentence)  

            **News Content**:  
            {text}  

            **Output Format**:  
            Sentiment: [Classification]  
            Assets: [Comma-separated symbols]  
            Reason: [Concise justification]  
        """
        body = json.dumps({
            "prompt": prompt,
            "max_gen_len": 2000,
            "temperature": 0.0
        })
        response = bedrock.invoke_model(
            modelId="arn:aws:bedrock:us-east-2:247140043804:inference-profile/us.meta.llama3-2-90b-instruct-v1:0",
            body=body,
            accept="application/json",
            contentType="application/json"
        )
        result = json.loads(response['body'].read())
        generation = result.get('generation', '').strip()
        print("generation", generation)
        if not generation:
            return {"error": "No generation in response."}
        # Parse the output for Sentiment, Assets, Reason
        sentiment, assets, reason = None, None, None
        for line in generation.splitlines():
            line = line.strip()
            if not line or ':' not in line:
                continue
            if line.lower().startswith('sentiment:'):
                sentiment = line.split(':', 1)[1].strip()
            elif line.lower().startswith('assets:'):
                assets = line.split(':', 1)[1].strip()
            elif line.lower().startswith('reason:'):
                reason = line.split(':', 1)[1].strip()
        return {"sentiment": sentiment, "assets": assets, "reason": reason, "raw": generation}
    except Exception as e:
        return {"error": str(e)}

# Streamlit UI
st.set_page_config(page_title="URL Sentiment Analyzer", page_icon="🔍", layout="centered")
st.title("🔍 URL Sentiment Analyzer with Bedrock Llama 3.2 Vision")
st.write("Enter a URL to analyze the sentiment of its content using a state-of-the-art LLM.")

url = st.text_input("Enter URL:", placeholder="https://example.com")

if url:
    with st.spinner("Fetching content..."):
        content = fetch_url_content(url)
    if content.startswith("Error fetching content"):
        st.error(content)
    else:
        st.subheader("Extracted Content:")
        st.write(content[:5000] + ("..." if len(content) > 5000 else ""))
        with st.spinner("Analyzing sentiment with Llama 3.2 90B Vision Instruct..."):
            result = analyze_sentiment_bedrock(content[:2000])
        if "error" in result:
            st.error(f"Error: {result['error']}")
        else:
            sentiment = result.get("sentiment")
            assets = result.get("assets", "None identified")
            reason = result.get("reason", "No reason provided.")
            st.success(f"**Sentiment:** {sentiment if sentiment else 'Not found'}")
            st.info(f"**Assets:** {assets}")
            st.write(f"**Reason:** {reason}")
            # Creative visualization
            if isinstance(sentiment, str) and sentiment:
                s = sentiment.lower()
                if s.startswith("strong positive"):
                    st.markdown(":rocket: **Strong Positive!** :star2:")
                    st.progress(100, text="Strong Positive")
                elif s.startswith("moderate positive"):
                    st.markdown(":sunny: **Moderate Positive!** :smile:")
                    st.progress(80, text="Moderate Positive")
                elif s.startswith("neutral"):
                    st.markdown(":foggy: **Neutral.** :neutral_face:")
                    st.progress(50, text="Neutral")
                elif s.startswith("moderate negative"):
                    st.markdown(":cloud_with_rain: **Moderate Negative!** :disappointed:")
                    st.progress(30, text="Moderate Negative")
                elif s.startswith("strong negative"):
                    st.markdown(":skull: **Strong Negative!** :scream:")
                    st.progress(10, text="Strong Negative")
                else:
                    st.markdown(f"**Sentiment:** {sentiment}")
                st.balloons()
            else:
                st.warning("Could not determine sentiment from model output. Please check the prompt or try again.")
else:
    st.info("Please enter a URL above to get started.")
