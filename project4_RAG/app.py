import os
import streamlit as st
from openai import OpenAI  # Updated OpenAI client
from pinecone import Pinecone, ServerlessSpec
import boto3
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize clients with explicit checks
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
BEDROCK_MODEL_ID = "meta.llama3-3-70b-instruct-v1:0"

# Validate environment variables
if not all([OPENAI_API_KEY, PINECONE_API_KEY]):
    st.error("Missing API keys. Check .env file or environment variables")
    st.stop()

# Initialize clients
pc = Pinecone(api_key=PINECONE_API_KEY)
openai_client = OpenAI(api_key=OPENAI_API_KEY)  # Updated client initialization
bedrock = boto3.client(
    service_name="bedrock-runtime",
    region_name="us-east-2"
)

# Initialize Pinecone index
index_name = "zhiyin"
if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=3072,  # Must match embedding dimension
        metric="cosine",
        spec=ServerlessSpec(cloud='aws', region='us-east-1')
    )
index = pc.Index(index_name)

def retrieve_crystals(query, top_k=3):
    # Updated embedding call
    response = openai_client.embeddings.create(
        model="text-embedding-3-large",
        input=query
    )
    embedding = response.data[0].embedding
    # Query with explicit namespace
    return index.query(
        vector=embedding,
        top_k=top_k,
        include_metadata=True,
        namespace="crystals"  # Add namespace if used
    ).matches

def format_context(matches):
    context = ""
    references = []
    for m in matches:
        meta = m["metadata"]
        context += f"Name: {meta.get('chinese_name', '')} ({meta.get('english_name', '')})\n"
        context += f"Color: {meta.get('color', '')}\n"
        context += f"General Effects: {meta.get('general_effects', '')}\n"
        context += f"Physiological Effects: {', '.join(meta.get('physiological_effects', []))}\n"
        context += f"Emotional Effects: {', '.join(meta.get('emotional_effects', []))}\n"
        context += f"Usage: {meta.get('usage', '')}\n"
        context += f"Zodiac: {', '.join(meta.get('zodiac', []))}\n"
        context += f"Chakras: {', '.join(meta.get('chakras', []))}\n"
        context += f"---\n"
        references.append(meta.get('english_name', ''))
    return context, references

def call_bedrock_llama3(user_query, context):
    prompt = f"""
You are a crystal recommendation expert. Based on the following crystal information and the user's question, recommend the most suitable crystal(s) to the user.

Return your answer as bullet points. Each bullet point should:
- Start with the crystal name (in bold if possible)
- Give a concise explanation of why it is recommended
- End with a reference to the crystal name in parentheses

Do not include any extra narrative or introduction. Only return the bullet points.

Context:
{context}

User question: {user_query}

Your answer:
"""
    body = {
        "prompt": prompt,
        "max_gen_len": 512,
        "temperature": 0.3,
        "top_p": 0.9
    }
    response = bedrock.invoke_model(
        modelId=BEDROCK_MODEL_ID,
        body=json.dumps(body),
        contentType="application/json"
    )
    result = json.loads(response["body"].read())
    return result["generation"] if "generation" in result else result.get("outputs", [{}])[0].get("text", "No response.")

# Streamlit UI
st.set_page_config(page_title="Crystal RAG Chatbot", page_icon="💎")
st.title("💎 Crystal RAG Chatbot")
st.write("Ask for crystal recommendations and get expert answers with reasons and references!")

# New input boxes for user info
user_name = st.text_input("Your Name:")
birth_day = st.date_input("Your Birthday:")

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

user_input = st.text_input("What do you want a crystal for? (e.g., stress relief, love, energy)")

if st.button("Ask") and user_input:
    with st.spinner("Retrieving recommendations..."):
        matches = retrieve_crystals(user_input, top_k=3)
        context, references = format_context(matches)
        answer = call_bedrock_llama3(user_input, context)
        # Store user info with chat history for future use
        st.session_state["chat_history"].append((user_input, answer, references, user_name, str(birth_day)))

st.write("---")
st.subheader("Chat History")
for i, item in enumerate(st.session_state["chat_history"][::-1]):
    # Support old and new tuple formats
    if len(item) == 5:
        q, a, refs, name, bday = item
        st.markdown(f"**You ({name}, {bday}):** {q}")
    else:
        q, a, refs = item
        st.markdown(f"**You:** {q}")
    st.markdown(f"**Bot:** {a}")
    st.write("") 