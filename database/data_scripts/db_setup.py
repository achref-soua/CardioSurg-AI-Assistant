from dotenv import load_dotenv
import os
import json
from transformers import AutoModel, AutoTokenizer
import torch
import chromadb

# Load environment variables from .env file
load_dotenv()

# Using a persistent client to save data locally
db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "chroma_db"))

# Use PersistentClient with that path
client = chromadb.PersistentClient(path=db_path)

# Define the embedding model and tokenizer
embedding_model_name = "BAAI/bge-large-en-v1.5"
embedding_model = AutoModel.from_pretrained(
    embedding_model_name, trust_remote_code=True
)
tokenizer = AutoTokenizer.from_pretrained(embedding_model_name, trust_remote_code=True)


def embed_text_transformers(text):
    """Generates an embedding for the given text using the specified model."""
    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
    with torch.no_grad():
        outputs = embedding_model(**inputs)
        # mean pooling to get a single vector
        embedding = outputs.last_hidden_state.mean(dim=1).squeeze().tolist()
    return embedding


def upload_with_embeddings(collection_name, json_path, text_key):
    """
    Loads documents from a JSON file, generates embeddings from a specified text key,
    and uploads them to a ChromaDB collection. Converts complex metadata values
    to strings to comply with ChromaDB's schema.

    Args:
        collection_name (str): The name of the ChromaDB collection.
        json_path (str): The path to the JSON file containing the documents.
        text_key (str): The key in the JSON documents whose value is used for embedding.
    """
    try:
        collection = client.get_or_create_collection(name=collection_name)
    except Exception as e:
        print(f"Error getting/creating collection '{collection_name}': {e}")
        return

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not data:
        print(f"No data found in {json_path}. Skipping upload.")
        return

    documents = []
    embeddings = []
    metadatas = []
    ids = []

    for i, doc in enumerate(data):
        text = doc.get(text_key, "")

        if text:
            try:
                embedding = embed_text_transformers(text)
                # Create a new metadata dictionary with flattened values
                cleaned_metadata = {}
                for key, value in doc.items():
                    if isinstance(value, (str, int, float, bool)):
                        cleaned_metadata[key] = value
                    else:
                        # Convert any complex type to a string
                        cleaned_metadata[key] = json.dumps(value)

                metadatas.append(cleaned_metadata)
                documents.append(text)
                embeddings.append(embedding)
                ids.append(str(i))
            except Exception as e:
                print(f"Could not embed document {i}: {e}")

    if not embeddings:
        print(
            f"Error: No embeddings were generated for collection '{collection_name}' from '{json_path}'."
        )
        return

    try:
        collection.add(
            documents=documents, embeddings=embeddings, metadatas=metadatas, ids=ids
        )
        print(f"Uploaded {len(documents)} documents to '{collection_name}'")
    except Exception as e:
        print(f"Error adding documents to collection '{collection_name}': {e}")


# --- Main execution ---
if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, "../preprocessed_data")

    # All collections now use the 'text' key
    collections = ["patients", "notes", "devices", "guidelines", "literature"]

    for collection_name in collections:
        json_path = os.path.join(data_dir, f"{collection_name}.json")
        upload_with_embeddings(
            collection_name=collection_name, json_path=json_path, text_key="text"
        )
