import streamlit as st
import boto3
import json
import os

# Model options and mapping
MODEL_OPTIONS = {
    "Llama 3.3 70B Instruct": "meta.llama3-3-70b-instruct-v1:0",
    "Llama 3.2 11B Vision Instruct": "arn:aws:bedrock:us-east-2:247140043804:inference-profile/us.meta.llama3-2-11b-instruct-v1:0",
    "Nova Lite": "arn:aws:bedrock:us-east-2:247140043804:inference-profile/us.amazon.nova-lite-v1:0"
}

REGION = "us-east-2"  # Change if needed
MEMORY_FILE = "chat_memory.json"

# Sidebar for model selection
st.sidebar.title("Model Selection")
selected_model_name = st.sidebar.radio(
    "Choose a model:", list(MODEL_OPTIONS.keys()), key="model_select"
)
BEDROCK_MODEL_ID = MODEL_OPTIONS[selected_model_name]

# Initialize Bedrock client
@st.cache_resource(show_spinner=False)
def get_bedrock_client():
    try:
        return boto3.client("bedrock-runtime", region_name=REGION)
    except Exception as e:
        st.error(f"Error initializing Bedrock client: {e}")
        return None

def query_llm(prompt, bedrock, model_id):
    try:
        response = bedrock.invoke_model(
            modelId=model_id,
            body=json.dumps({"prompt": prompt}).encode("utf-8"),
            accept="application/json",
            contentType="application/json"
        )
        result = json.loads(response["body"].read())

        # Adjust this if the response format is different
        return result["generation"]
    except Exception as e:
        st.error(f"Error querying LLM: {e}")
        return "[Error: Could not get response from LLM.]"

# Helper functions for memory persistence
def save_memory(memory):
    try:
        with open(MEMORY_FILE, "w", encoding="utf-8") as f:
            json.dump(memory, f, ensure_ascii=False, indent=2)
    except Exception as e:
        st.error(f"Error saving memory: {e}")

def load_memory():
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            st.error(f"Error loading memory: {e}")
    return []

# Streamlit UI
st.set_page_config(page_title="Chatbot With Memory", page_icon="🤖")
st.title("🤖 Bedrock Chatbot with Local Memory")

# Initialize session state for chat history
if "memory" not in st.session_state:
    st.session_state.memory = []  # UI always starts empty

# Only display the latest bot response (if any and session is not new)
if st.session_state.memory:
    # Check if there is at least one user message
    has_user_message = any(m["role"] == "user" for m in st.session_state.memory)
    last_msg = st.session_state.memory[-1]
    if has_user_message and last_msg["role"] == "assistant":
        st.markdown(f"**Bot:** {last_msg['content']}")

# User input
user_input = st.text_input("Type your message:", key="input")
if st.button("Send") and user_input.strip():
    # Load persistent memory for context
    persistent_memory = load_memory()
    persistent_memory.append({"role": "user", "content": user_input})
    # Use last 5 turns as context (or all if less than 5)
    context = "\n".join([f"{m['role']}: {m['content']}" for m in persistent_memory[-5:]])
    prompt = f"{context}\nassistant:"
    bedrock = get_bedrock_client()
    if bedrock:
        response = query_llm(prompt, bedrock, BEDROCK_MODEL_ID)
        persistent_memory.append({"role": "assistant", "content": response})
        save_memory(persistent_memory)  # Save after bot response
        # Only show the latest exchange in the UI
        st.session_state.memory = [
            {"role": "user", "content": user_input},
            {"role": "assistant", "content": response}
        ]
        st.rerun()

# Option to clear chat
if st.button("Clear Chat"):
    st.session_state.memory = []
    save_memory([])
    st.rerun()
