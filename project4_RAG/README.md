# Crystal RAG Chatbot

A Retrieval-Augmented Generation (RAG) chatbot for recommending crystals, built with Streamlit. It uses OpenAI for embeddings, Pinecone for vector search, and AWS Bedrock Llama 3 70B Instruct for generating expert, referenced recommendations.

## Features
- **Chatbot UI**: Ask for crystal recommendations (e.g., for stress relief, love, energy, etc.)
- **RAG Pipeline**: Retrieves relevant crystal data and generates answers with reasons and references
- **Data-backed**: Uses a curated dataset of crystals with rich metadata

## Architecture
- **Embeddings**: OpenAI `text-embedding-3-large`
- **Vector DB**: Pinecone
- **LLM**: AWS Bedrock Llama 3 70B Instruct (`meta.llama3-3-70b-instruct-v1:0`)
- **Frontend**: Streamlit

## Setup Instructions

### 1. Clone the repository and enter the project folder
```
cd AIPI561_Projects/project4_RAG
```

### 2. Prepare your environment
Run the setup script (Windows):
```
setup.bat
```
This will create a virtual environment and install all dependencies from `requirements.txt`.

Also remember to login aws CLI service using`aws configure`.

### 3. Configure your API keys
Create a `.env` file in this directory with the following variables:
```
PINECONE_API_KEY=your-pinecone-api-key
OPENAI_API_KEY=your-openai-api-key
```

### 4. Prepare and upload the crystal data to Pinecone
- Edit or add your crystal data in `data/crystals.json` (see format below).
- Run the data upload script:
```
python upload_crystals.py
```
This will embed the crystal data and upload it to your Pinecone index.

### 5. Run the Streamlit chatbot
```
streamlit run streamlit_app.py
```
Open the provided local URL in your browser to chat with the RAG bot.

## Data Format (`data/crystals.json`)
The file should look like:
```json
{
  "crystals": [
    {
      "color": "白色",
      "chinese_name": "白水晶",
      "english_name": "Quartz crystal",
      "intro": "...",
      "effects": {
        "general": "...",
        "physiological": ["..."],
        "emotional": ["..."]
      },
      "usage": "...",
      "purification": ["..."],
      "hardness": null,
      "origins": ["..."],
      "aliases": ["..."],
      "zodiac": ["..."],
      "chakras": ["..."],
      "match": [],
      "five_elements": ""
    },
    ...
  ]
}
```
Each crystal entry contains rich metadata for retrieval and reference.

## Customization
- Add or edit crystals in `data/crystals.json`.
- Adjust retrieval or prompt logic in `app.py` as needed.

## Troubleshooting
- Ensure your Pinecone, OpenAI, and AWS credentials are correct and active.
- If you change the data, re-run `upload_crystals.py` to update Pinecone.
- For AWS Bedrock, make sure your account has access to the Llama 3 70B Instruct model in the specified region.

## License
MIT
