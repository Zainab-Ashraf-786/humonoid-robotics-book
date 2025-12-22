import os
Create a test script at backend/scripts/test_rag.py that:

1. Tests the ingestion:
   - Verifies connection to Qdrant
   - Checks if book_content collection exists
   - Shows count of vectors stored

2. Tests retrieval:
   - Takes a sample question
   - Queries Qdrant for relevant chunks
   - Displays the retrieved text

3. Tests chat endpoint:
   - Makes POST request to /chat with test question
   - Displays the response

4. Tests selection endpoint:
   - Makes POST request to /chat-selection with sample text and question
   - Displays the response

5. Tests database:
   - Verifies connection to Neon
   - Creates test session
   - Saves test message
   - Retrieves chat history

Include clear output showing what's working and what's not.import httpx
from typing import List, Dict
from dotenv import load_dotenv
from .query import semantic_search

# Load environment variables
load_dotenv()

def generate_rag_response(user_question: str, context_chunks: List[Dict] = None) -> str:
    """
    Generate a response using Retrieval-Augmented Generation (RAG)

    Args:
        user_question: The question from the user
        context_chunks: Retrieved context chunks from semantic search (if not provided, will perform search)

    Returns:
        str: Generated response from the LLM
    """
    # If context_chunks not provided, perform semantic search
    if context_chunks is None:
        context_chunks = semantic_search(user_question, top_k=5)

    # Format context from retrieved chunks
    context_str = ""
    for idx, chunk in enumerate(context_chunks):
        score = chunk.get('score', 0)
        content = chunk.get('content', '')
        context_str += f"[Chunk {idx+1} (Relevance: {score:.2f})]\n{content}\n\n"

    # If no context found, use a fallback approach
    if not context_str.strip():
        context_str = "No relevant context found in the documents."

    # Create the system prompt to guide the model's behavior
    system_message = f"""You are an expert assistant for the Physical AI & Humanoid Robotics course.
Your role is to help students understand concepts related to ROS 2, Gazebo, Unity, NVIDIA Isaac, Physical AI,
embodied intelligence, and humanoid robotics. Use the provided context to answer the user's question accurately
and comprehensively. If the context doesn't contain relevant information, acknowledge this and provide
general guidance about where they might find the information in the course structure.
Be helpful, educational, and focused on robotics and AI concepts."""

    # Create the user message with context
    user_message = f"""Context Information:
{context_str}

User Question: {user_question}

Please provide a helpful, accurate response based on the context provided. If the context doesn't contain
relevant information, let the user know and suggest where they might find the information in the course structure."""

    # OpenRouter model selection with priority order
    available_models = [
        "qwen/qwen-2.5-7b-instruct",
        "google/gemma-2-9b-it",
        "deepseek/deepseek-chat",
        "meta-llama/llama-3.1-8b-instruct"
    ]

    # Try models in priority order
    for model in available_models:
        try:
            response = call_openrouter_api(model, system_message, user_message)
            return response
        except httpx.HTTPStatusError as e:
            if e.response.status_code in [404, 401, 422]:
                # Try the next model in the list
                continue
            else:
                # For other errors, re-raise
                raise
        except Exception as e:
            # For other exceptions, try the next model
            print(f"Error with model {model}: {str(e)}")
            continue

    # If all models fail, raise an error
    raise Exception("All models failed to respond")

def call_openrouter_api(model: str, system_message: str, user_message: str) -> str:
    """
    Call the OpenRouter API directly using HTTP requests

    Args:
        model: The model to use
        system_message: System message to guide behavior
        user_message: User message with context
    Returns:
        str: Generated response from the model
    """
    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:8000",
        "X-Title": "Humanoid Robotics Book Chatbot"
    }

    data = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message}
        ],
        "temperature": 0.3,  # Lower temperature for more factual responses
        "max_tokens": 1000,  # Adjust based on expected response length
        "top_p": 1.0,
        "frequency_penalty": 0.0,
        "presence_penalty": 0.0
    }

    with httpx.Client(timeout=30.0) as client:
        response = client.post(url, headers=headers, json=data)
        response.raise_for_status()

        result = response.json()
        return result['choices'][0]['message']['content']

def chat_with_rag(user_question: str, top_k: int = 5) -> Dict:
    """
    Main chat function that performs semantic search and generates response

    Args:
        user_question: Question from the user
        top_k: Number of top context chunks to retrieve

    Returns:
        Dict: Response with answer and source information
    """
    # Perform semantic search to find relevant context
    search_results = semantic_search(user_question, top_k=top_k)

    # Generate the RAG response
    answer = generate_rag_response(user_question, search_results)

    # Prepare response with source information
    sources = []
    for result in search_results:
        sources.append({
            "content_snippet": result.get("content", "")[:200] + "...",  # First 200 chars plus ellipsis
            "relevance_score": result.get("score", 0),
            "document_id": result.get("id", "")
        })

    response = {
        "answer": answer,
        "sources": sources,
        "query": user_question,
        "num_sources": len(sources)
    }

    return response

def validate_openrouter_connection():
    """
    Validate that the OpenRouter API key is working with a test call
    """
    try:
        # Try the default model or first available model
        model = os.getenv("OPENROUTER_MODEL", "qwen/qwen-2.5-7b-instruct")

        response = call_openrouter_api(
            model=model,
            system_message="You are a test assistant.",
            user_message="Say 'connection successful' in one word."
        )

        return "successful" in response.lower()
    except Exception as e:
        print(f"OpenRouter API validation failed: {str(e)}")
        return False