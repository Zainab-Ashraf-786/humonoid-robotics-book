import os
import cohere
from dotenv import load_dotenv
import numpy as np
from qdrant_client.http import models
from sentence_transformers import SentenceTransformer

# Load environment variables
load_dotenv()

# Initialize Cohere client
cohere_api_key = os.getenv("COHERE_API_KEY")
if not cohere_api_key:
    raise ValueError("COHERE_API_KEY must be set in environment variables")

co = cohere.Client(cohere_api_key)

# Initialize sentence transformer model that matches ingestion (384 dim)
embedder = SentenceTransformer('all-MiniLM-L6-v2')

def generate_embedding(text: str, model: str = "embed-english-v3.0", input_type: str = "search_document"):
    """
    Generate embeddings for the given text using local model (matching query)

    Args:
        text: Input text to embed
        model: Cohere embedding model to use (not used when using local model)
        input_type: Type of input (not used when using local model)

    Returns:
        List[float]: Embedding vector
    """
    if not text.strip():
        return [0.0] * 384  # Return zero vector for empty text

    # Generate embedding with local model that matches query embeddings
    embedding = embedder.encode([text])[0].tolist()
    return embedding

def generate_query_embedding(query: str, model: str = "embed-english-v3.0"):
    """
    Generate embeddings for query text using local model (matching ingestion)

    Args:
        query: Query text to embed
        model: Cohere embedding model to use (not used when using local model)

    Returns:
        List[float]: Embedding vector
    """
    if not query.strip():
        return [0.0] * 384  # Return zero vector for empty query

    # Generate embedding with local model that matches ingestion
    embedding = embedder.encode([query])[0].tolist()
    return embedding

def normalize_vector(vec):
    """
    Normalize a vector to unit length
    """
    vec_array = np.array(vec)
    norm = np.linalg.norm(vec_array)
    if norm == 0:
        return vec
    return (vec_array / norm).tolist()