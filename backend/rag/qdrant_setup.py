import os
from qdrant_client import QdrantClient
from qdrant_client.http import models
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_qdrant_client():
    """
    Creates and returns a Qdrant client instance
    """
    qdrant_url = os.getenv("QDRANT_URL")
    qdrant_api_key = os.getenv("QDRANT_API_KEY")

    if not qdrant_url or not qdrant_api_key:
        raise ValueError("QDRANT_URL and QDRANT_API_KEY must be set in environment variables")

    client = QdrantClient(
        url=qdrant_url,
        api_key=qdrant_api_key,
        https=True
    )
    
    return client

def setup_qdrant_collection():
    """
    Creates the 'book_content' collection in Qdrant if it doesn't exist
    """
    client = get_qdrant_client()
    
    # Check if collection exists
    collections = client.get_collections().collections
    collection_names = [collection.name for collection in collections]
    
    if "book_content" not in collection_names:
        # Create the collection with specified parameters
        client.create_collection(
            collection_name="book_content",
            vectors_config=models.VectorParams(
                size=384,  # Local embedding size (all-MiniLM-L6-v2)
                distance=models.Distance.COSINE
            )
        )
        print("Created 'book_content' collection in Qdrant")
    else:
        print("'book_content' collection already exists in Qdrant")

    # Configure the collection
    client.update_collection(
        collection_name="book_content",
        optimizer_config=models.OptimizersConfigDiff(
            memmap_threshold=20000,
            indexing_threshold=20000
        ),
        hnsw_config=models.HnswConfigDiff(
            m=16,
            ef_construct=100,
            ef=10,
            pq=models.ProductQuantization(
                enabled=False
            ),
            vector_data_type=models.VectorDataType.FLOAT32
        )
    )
    
    return client

if __name__ == "__main__":
    setup_qdrant_collection()