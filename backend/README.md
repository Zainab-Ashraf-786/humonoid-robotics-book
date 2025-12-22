# Backend Scripts for Physical AI & Humanoid Robotics Course

This directory contains backend scripts for managing and processing the course content, including the Qdrant vector database setup and book content ingestion.

## Book Content Ingestion

The ingestion script processes your book content files and loads them into a Qdrant vector database for RAG (Retrieval Augmented Generation) applications.

### Setup Requirements

1. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up your environment variables by copying .env.example to .env:
   ```bash
   cp .env.example .env
   ```
   
3. Update the .env file with your actual credentials:
   - `QDRANT_URL`: Your Qdrant Cloud cluster URL
   - `QDRANT_API_KEY`: Your Qdrant Cloud API key
   - `COHERE_API_KEY`: Your Cohere API key

### Running the Ingestion Script

To ingest your book content into the Qdrant database:

1. Place your book content files (.txt, .md, .pdf) in a directory (default is `book-content/`)

2. Run the ingestion script:
   ```bash
   python -m scripts.ingest_book
   # OR specify a custom content directory:
   python -m scripts.ingest_book path/to/your/content
   ```

### Supported File Formats

- `.txt` - Plain text files
- `.md` - Markdown files
- `.pdf` - PDF documents

The script will process all supported files in the content directory recursively.

### Content Processing

The ingestion script will:
1. Read each file and extract its content
2. Split content into 500-1000 character chunks with 100-character overlap
3. Preserve paragraph boundaries during chunking
4. Generate embeddings using Cohere's `embed-english-v3.0` model (1024 dimensions)
5. Store content, embeddings, and metadata in Qdrant collection named "course_embeddings"
6. Maintain metadata including source file, chunk index, and position

### Configuration

- **Chunk size**: 500-1000 characters (target ~800)
- **Overlap**: 100 characters between adjacent chunks
- **Vector dimensions**: 1024 (matching Cohere's embedding model)
- **Distance metric**: COSINE (for semantic similarity)
- **Batch size**: 10 items per batch for efficient processing

## Qdrant Vector Database

The script creates and populates a Qdrant collection optimized for:
- Semantic search of course content
- RAG applications for the course chatbot
- High-performance similarity search
- Scalable storage of course embeddings

### Collection Schema

- **Vectors**: 1024-dimension vectors using Cohere embeddings
- **Payload Fields**:
  - `text`: Original content chunk
  - `metadata`: Contains source_file, source_name, chunk_idx, start_pos, end_pos, etc.

## Troubleshooting

If the ingestion fails, check:
1. All required environment variables are properly set
2. Your Qdrant cluster is accessible and credentials are correct
3. You have sufficient permissions for the Qdrant collection
4. Your Cohere API key has proper embedding permissions
5. Your content directory exists and contains supported file formats

For additional help, run:
```bash
python -m scripts.ingest_book --help
```