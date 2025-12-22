# Testing the Ingestion Script Setup

To verify that the ingestion script is properly set up:

## 1. Create a sample content directory
```bash
mkdir book-content
echo "# Sample Course Content

This is a sample document to test the ingestion script.

## Module 1: The Robotic Nervous System

ROS 2 provides the communication backbone for robotic systems.

### Nodes, Topics, Services, and Actions

These are fundamental concepts in ROS 2..." > book-content\sample.md
```

## 2. Set up environment variables
Create a .env file with your actual credentials:
```bash
QDRANT_URL=your_actual_qdrant_url
QDRANT_API_KEY=your_actual_qdrant_api_key
COHERE_API_KEY=your_actual_cohere_api_key
```

## 3. Run the ingestion script
```bash
cd backend
python scripts/ingest_book.py book-content
```

The script will:
1. Connect to your Qdrant instance
2. Create a collection named "book_content" with 1024-dimension vectors
3. Process all .txt, .md, and .pdf files in the content directory
4. Generate embeddings using Cohere
5. Upload the content and embeddings to Qdrant with appropriate metadata

## Expected Output
If successful, you should see:
- Connection to Qdrant established successfully
- Collection created or confirmed to exist
- Content files processed and chunked appropriately
- Embeddings generated and uploaded to Qdrant
- Final confirmation message with total chunks ingested