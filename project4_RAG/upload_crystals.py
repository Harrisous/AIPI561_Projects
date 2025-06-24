import os
import json
import re
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
from tqdm import tqdm
from openai import OpenAI

# Initialize Pinecone
load_dotenv()
pinecone = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
client = OpenAI(api_key = os.getenv("OPENAI_API_KEY"))

# Create or get index
index_name = "zhiyin"
dimension = 3072  # OpenAI embeddings dimension

# Create index if it doesn't exist
if index_name not in pinecone.list_indexes().names():
    pinecone.create_index(
        name=index_name,
        dimension=dimension,
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1"
        ) 
    )

# Get the index
index = pinecone.Index(index_name)

# Delete all existing vectors from the index
print("Deleting existing vectors from Pinecone index...")
try:
    # First try to get index stats to see if there are any vectors
    stats = index.describe_index_stats()
    if stats.total_vector_count > 0:
        # Only attempt deletion if there are vectors
        index.delete(delete_all=True)
    print("Existing vectors deleted successfully.")
except Exception as e:
    print(f"No existing vectors to delete: {str(e)}")

print("Current index stats:")
print(index.describe_index_stats())

def create_ascii_id(name):
    """Convert a string to an ASCII-compatible ID by replacing special characters with underscores"""
    # Replace special characters with underscores
    ascii_id = re.sub(r'[^a-zA-Z0-9]', '_', name)
    # Remove multiple consecutive underscores
    ascii_id = re.sub(r'_+', '_', ascii_id)
    # Remove leading and trailing underscores
    ascii_id = ascii_id.strip('_')
    return ascii_id

def clean_metadata_value(value):
    """Convert null values to empty strings and ensure lists contain only strings"""
    if value is None:
        return ""
    if isinstance(value, list):
        return [str(item) for item in value if item is not None]
    return str(value)

def read_documents():
    # Get the absolute path to the project root directory
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    json_path = os.path.join(project_root, 'data', 'crystals.json')

    # Load crystal data
    with open(json_path, 'r', encoding='utf-8') as f:
        crystal_data = json.load(f)

    # Prepare documents for upload
    documents = []
    for crystal in tqdm(crystal_data['crystals'], desc="Processing crystals"):
        # Create a text representation of the crystal
        text = f"""
        Name: {crystal['chinese_name']} ({crystal['english_name']})
        Color: {crystal['color']}
        Introduction: {crystal['intro']}
        General Effects: {crystal['effects']['general']}
        Physiological Effects: {', '.join(crystal['effects'].get('physiological', []))}
        Emotional Effects: {', '.join(crystal['effects'].get('emotional', []))}
        Usage: {crystal['usage'] if isinstance(crystal['usage'], str) else crystal['usage'].get('when_to_use', '')}
        Zodiac Signs: {', '.join(crystal.get('zodiac', []))}
        Chakras: {', '.join(crystal.get('chakras', []))}
        """
        
        # Create comprehensive metadata with cleaned values
        metadata = {
            'chinese_name': clean_metadata_value(crystal['chinese_name']),
            'english_name': clean_metadata_value(crystal['english_name']),
            'color': clean_metadata_value(crystal['color']),
            'hardness': clean_metadata_value(crystal.get('hardness')),
            'origins': clean_metadata_value(crystal.get('origins', [])),
            'zodiac': clean_metadata_value(crystal.get('zodiac', [])),
            'chakras': clean_metadata_value(crystal.get('chakras', [])),
            'matching_luckstone': clean_metadata_value(crystal.get('matching_luckstone', [])),
            'intro': clean_metadata_value(crystal['intro']),
            'general_effects': clean_metadata_value(crystal['effects']['general']),
            'physiological_effects': clean_metadata_value(crystal['effects'].get('physiological', [])),
            'emotional_effects': clean_metadata_value(crystal['effects'].get('emotional', [])),
            'usage': clean_metadata_value(crystal['usage'] if isinstance(crystal['usage'], str) else crystal['usage'].get('when_to_use', '')),
            'purification': clean_metadata_value(crystal.get('purification', [])),
            'aliases': clean_metadata_value(crystal.get('aliases', [])),
            'five_elements': clean_metadata_value(crystal.get('five_elements'))
        }
        
        documents.append({
            'text': text,
            'metadata': metadata,
            'id': create_ascii_id(crystal['english_name'])
        })
        
    return documents

def upload_document_embeddings(documents):
    # Create embeddings and upload to Pinecone
    print("Creating embeddings and uploading to Pinecone...")
    for doc in tqdm(documents, desc="Uploading to Pinecone"):
        # Create embedding
        response = client.embeddings.create(
            model="text-embedding-3-large",
            input=doc['text'],
            encoding_format="float"
        )
        embedding = response.data[0].embedding
        
        # Upload to Pinecone
        index.upsert(
            vectors=[{
                'id': doc['id'],
                'values': embedding,
                'metadata': doc['metadata']
            }]
        )

    print("Upload complete!")

if __name__ == "__main__":
    documents = read_documents()
    upload_document_embeddings(documents)
