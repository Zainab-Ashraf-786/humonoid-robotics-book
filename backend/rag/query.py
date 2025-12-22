import uuid
from typing import List, Dict
from qdrant_client.http import models
from .qdrant_setup import get_qdrant_client
from .embed import generate_query_embedding, generate_embedding

def semantic_search(query: str, top_k: int = 5) -> List[Dict]:
    """
    Perform semantic search in the Qdrant collection using the query
    """
    client = get_qdrant_client()

    # Generate embedding for the query
    query_embedding = generate_query_embedding(query)

    # Perform semantic search in Qdrant using new query_points method
    search_results = client.query_points(
        collection_name="book_content",  # Fixed
        query=query_embedding,  # Renamed from query_vector
        limit=top_k,
        with_payload=True,
        score_threshold=0.3
    ).points  # Results are now in .points

    # Format results
    formatted_results = []
    for hit in search_results:
        formatted_results.append({
            "score": hit.score,
            "content": hit.payload.get("content", "") if hit.payload else "",
            "metadata": hit.payload.get("metadata", {}) if hit.payload else {},
            "id": hit.id
        })

    return formatted_results

def insert_document(content: str, metadata: Dict = None, doc_id: str = None) -> str:
    client = get_qdrant_client()
    if not doc_id:
        doc_id = str(uuid.uuid4())
    if not metadata:
        metadata = {}
    embedding = generate_embedding(content)
    client.upsert(
        collection_name="book_content",
        points=[{
            "id": doc_id,
            "vector": embedding,
            "payload": {
                "content": content,
                "metadata": metadata
            }
        }]
    )
    return doc_id

def batch_insert_documents(documents: List[Dict]) -> List[str]:
    client = get_qdrant_client()
    points = []
    doc_ids = []
    for doc in documents:
        content = doc.get("content", "")
        metadata = doc.get("metadata", {})
        doc_id = doc.get("id", str(uuid.uuid4()))
        embedding = generate_embedding(content)
        points.append({
            "id": doc_id,
            "vector": embedding,
            "payload": {
                "content": content,
                "metadata": metadata
            }
        })
        doc_ids.append(doc_id)
    client.upsert(collection_name="book_content", points=points)
    return doc_ids

def get_all_documents(top_k: int = None) -> List[Dict]:
    client = get_qdrant_client()
    results = client.scroll(
        collection_name="book_content",
        limit=top_k,
        with_payload=True
    )
    formatted_results = []
    for point, _ in results:
        formatted_results.append({
            "id": point.id,
            "content": point.payload.get("content", ""),
            "metadata": point.payload.get("metadata", {})
        })
    return formatted_results
