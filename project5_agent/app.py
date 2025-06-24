import streamlit as st
import os
from tavily import TavilyClient
import boto3
from dotenv import load_dotenv
import json

load_dotenv()

def is_duke_question(question):
    keywords = ["duke university", "duke", "durham", "blue devils", "duke campus", "duke student", "duke faculty", "duke research"]
    q = question.lower()
    return any(k in q for k in keywords)

# Initialize Tavily client (set your API key as TAVILY_API_KEY env variable)
tavily_api_key = os.getenv("TAVILY_API_KEY")
tavily_client = TavilyClient(api_key=tavily_api_key)

# Initialize Bedrock client (set AWS credentials in env or config)
bedrock = boto3.client(
    service_name="bedrock-runtime",
    region_name="us-east-2"  # Change if needed
)
BEDROCK_MODEL_ID = "meta.llama3-3-70b-instruct-v1:0"

def search_duke(query):
    # Use Tavily to search, restrict to Duke University
    search_query = f"site:duke.edu {query}"
    results = tavily_client.search(query=search_query, max_results=5)
    return "\n".join([r["content"] for r in results["results"]])

def ask_llm(context, question):
    prompt = f"You are an expert on Duke University. Only answer questions about Duke University. If the question is not about Duke, say 'I can only answer questions about Duke University.'\n\nContext:\n{context}\n\nQuestion: {question}\nAnswer: "
    body = {
        "prompt": prompt,
        "max_gen_len": 512,
        "temperature": 0.2,
        "top_p": 0.9
    }
    response = bedrock.invoke_model(
        modelId=BEDROCK_MODEL_ID,
        body=json.dumps(body).encode("utf-8")
    )
    raw = response["body"].read().decode("utf-8")
    data = json.loads(raw)
    return data["generation"].strip()

def main():
    st.title("Duke University Q&A Agent")
    st.write("Ask any question about Duke University!")
    question = st.text_input("Your question:")
    if question:
        if not is_duke_question(question):
            st.warning("I can only answer questions about Duke University.")
            return
        with st.spinner("Searching and answering..."):
            context = search_duke(question)
            answer = ask_llm(context, question)
            st.markdown(f"**Answer:** {answer}")

if __name__ == "__main__":
    main() 