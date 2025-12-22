from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, List, Dict
import logging
import uuid
from datetime import datetime
import os
import httpx
from app.database import DatabaseManager, get_db
from ..services.user_profile_service import UserProfileService

# Import semantic_search from your RAG module (this avoids direct QdrantClient.search error)
from rag.query import semantic_search

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

# --- Request & Response Models ---
class InnerRequest(BaseModel):
    message: str

class ChatRequest(BaseModel):
    request: Optional[InnerRequest] = None    # For nested: {"request": {"message": "..."}}
    message: Optional[str] = None             # For flat: {"message": "..."}
    session_id: Optional[str] = None
    top_k: Optional[int] = 5

class InnerSelectionRequest(BaseModel):
    selected_text: str
    question: str

class ChatSelectionRequest(BaseModel):
    request: Optional[InnerSelectionRequest] = None
    selected_text: Optional[str] = None
    question: Optional[str] = None
    session_id: Optional[str] = None

class SourceChunk(BaseModel):
    content: str
    score: float
    document_id: Optional[str] = None

class ChatResponse(BaseModel):
    answer: str
    session_id: str
    sources: List[SourceChunk]

# --- Helper Functions ---
def default_user_profile() -> dict:
    return {
        "experience_level": "beginner",
        "software_background": "general",
        "hardware_background": "general",
        "programming_languages": "not specified",
        "learning_goals": "general learning"
    }

async def retrieve_from_qdrant(query_text: str, top_k: int = 5) -> List[dict]:
    """Use your existing semantic_search function (which works correctly)"""
    try:
        search_results = semantic_search(query_text, top_k=top_k)
        relevant_chunks = []
        for result in search_results:
            relevant_chunks.append({
                "content": result.get("content", ""),
                "score": result.get("score", 0.0),
                "document_id": result.get("id")
            })
        logger.info(f"Retrieved {len(relevant_chunks)} chunks for query: {query_text[:50]}...")
        return relevant_chunks
    except Exception as e:
        logger.error(f"Error in retrieve_from_qdrant: {e}")
        return []  # Return empty on failure to avoid crashing

def build_full_context(user_message: str, chat_history: List[dict], relevant_chunks: List[dict], user_profile_context: Optional[dict] = None) -> str:
    context_parts = ["## User Profile:"]
    profile = user_profile_context or default_user_profile()
    for k, v in profile.items():
        context_parts.append(f"- {k.replace('_', ' ').capitalize()}: {v}")

    if relevant_chunks:
        context_parts.append("## Retrieved Information:")
        for i, c in enumerate(relevant_chunks):
            context_parts.append(f"### Source {i+1} (Score: {c['score']:.2f}):")
            context_parts.append(c['content'])

    if chat_history:
        context_parts.append("## Chat History:")
        for msg in chat_history:
            role = msg.get("role", "unknown").capitalize()
            content = msg.get("content", "")
            timestamp = msg.get("timestamp", "")
            context_parts.append(f"{role} ({timestamp}): {content}")

    context_parts.append("## User Question:")
    context_parts.append(user_message)
    return "\n".join(context_parts)

async def call_openrouter_api(system_message: str, user_message: str) -> str:
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="OPENROUTER_API_KEY not set")

    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:8000",
        "X-Title": "Humanoid Robotics Book Chatbot"
    }
    data = {
        "model": "qwen/qwen-2.5-7b-instruct",
        "messages": [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message}
        ],
        "temperature": 0.7,
        "max_tokens": 1000
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(url, headers=headers, json=data)
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail=f"OpenRouter error: {response.text}")
        return response.json()["choices"][0]["message"]["content"]

async def generate_response_with_context(
    user_message: str,
    chat_history: List[dict],
    relevant_chunks: List[dict],
    user_profile_context: Optional[dict] = None
) -> str:
    full_context = build_full_context(user_message, chat_history, relevant_chunks, user_profile_context)
    return await call_openrouter_api("You are a helpful AI assistant for Physical AI & Humanoid Robotics.", full_context)

# --- Endpoints ---
@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest, current_user: Optional[dict] = None, db: DatabaseManager = Depends(get_db)):
    try:
        user_id = current_user.get("id") if current_user else "anonymous"
        session_id = request.session_id or f"sess_{uuid.uuid4().hex[:8]}_{int(datetime.now().timestamp())}"

        # Extract message safely
        message = (request.request.get("message") if request.request else None) or request.message
        if not message:
            raise HTTPException(status_code=400, detail="Message is required")

        if db:
            if not request.session_id:
                await db.create_session(user_id=user_id)
            await db.save_message(session_id=session_id, role="user", content=message)

        relevant_chunks = await retrieve_from_qdrant(message, request.top_k or 5)
        chat_history = await db.get_chat_history(session_id, limit=10) if db else []

        user_profile_context = default_user_profile()
        if user_id != "anonymous" and db:
            try:
                profile_service = UserProfileService(db)
                user_profile_context = await profile_service.get_personalization_context(user_id)
            except Exception as e:
                logger.warning(f"User profile error: {e}")

        answer = await generate_response_with_context(message, chat_history, relevant_chunks, user_profile_context)

        if db:
            await db.save_message(session_id=session_id, role="assistant", content=answer)
            await db.update_session(session_id)

        sources = [
            SourceChunk(
                content=c["content"],
                score=c["score"],
                document_id=str(c.get("document_id"))  # Convert to string to match model
            )
            for c in relevant_chunks
        ]

        return ChatResponse(answer=answer, session_id=session_id, sources=sources)

    except Exception as e:
        logger.error(f"Chat endpoint error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/chat-selection", response_model=ChatResponse)
async def chat_selection_endpoint(request: ChatSelectionRequest, current_user: Optional[dict] = None, db: DatabaseManager = Depends(get_db)):
    try:
        user_id = current_user.get("id") if current_user else "anonymous"
        session_id = request.session_id or f"sess_{uuid.uuid4().hex[:8]}_{int(datetime.now().timestamp())}"

        # Extract selected_text and question from either nested or flat format
        if request.request and request.request.selected_text and request.request.question:
            selected_text = request.request.selected_text
            question = request.request.question
        elif request.selected_text and request.question:
            selected_text = request.selected_text
            question = request.question
        else:
            raise HTTPException(status_code=400, detail="selected_text and question are required")

        query_text = f"Regarding this text: '{selected_text}', {question}"

        if db:
            if not request.session_id:
                await db.create_session(user_id=user_id)
            await db.save_message(session_id=session_id, role="user", content=query_text)

        relevant_chunks = await retrieve_from_qdrant(query_text, top_k=5)
        chat_history = await db.get_chat_history(session_id, limit=10) if db else []

        user_profile_context = default_user_profile()
        if user_id != "anonymous" and db:
            try:
                profile_service = UserProfileService(db)
                user_profile_context = await profile_service.get_personalization_context(user_id)
            except Exception as e:
                logger.warning(f"User profile error: {e}")

        answer = await generate_response_with_context(query_text, chat_history, relevant_chunks, user_profile_context)

        if db:
            await db.save_message(session_id=session_id, role="assistant", content=answer)
            await db.update_session(session_id)

        sources = [
            SourceChunk(
                content=c["content"],
                score=c["score"],
                document_id=str(c.get("document_id"))  # Convert to string to match model
            )
            for c in relevant_chunks
        ]

        return ChatResponse(answer=answer, session_id=session_id, sources=sources)

    except Exception as e:
        logger.error(f"Chat selection endpoint error: {e}")
        raise HTTPException(status_code=500, detail=str(e))