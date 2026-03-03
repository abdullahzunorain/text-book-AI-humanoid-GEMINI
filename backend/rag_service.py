"""
RAG (Retrieval-Augmented Generation) service for generating AI responses.
Combines textbook context from Qdrant with chat history from Neon.
"""
from sqlalchemy.orm import Session
from qdrant_client import QdrantClient
from typing import List, Dict, Any, Optional
import os
from dotenv import load_dotenv
import requests
import json

from crud_vectors import search_textbook_content
from crud_messages import get_recent_chat_history

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"


class RAGService:
    """
    Service for generating RAG-based responses.
    """
    
    def __init__(self, db: Session, qdrant_client: QdrantClient):
        """
        Initialize RAG service.
        
        Args:
            db: Database session
            qdrant_client: Qdrant vector database client
        """
        self.db = db
        self.qdrant_client = qdrant_client
        
        if not GEMINI_API_KEY:
            raise ValueError(
                "GEMINI_API_KEY environment variable is not set. "
                "Please set it in your .env file."
            )
    
    def retrieve_context(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Retrieve relevant textbook context for a query.
        
        Args:
            query: User's query
            limit: Number of context pieces to retrieve
        
        Returns:
            List of relevant textbook segments
        """
        return search_textbook_content(
            client=self.qdrant_client,
            query=query,
            limit=limit,
            score_threshold=0.4
        )
    
    def format_chat_history(self, messages: List) -> str:
        """
        Format chat history for the prompt.
        
        Args:
            messages: List of Message objects
        
        Returns:
            Formatted chat history string
        """
        if not messages:
            return "No previous conversation."
        
        formatted = []
        for msg in reversed(messages[:10]):  # Last 10 messages
            role = "User" if msg.role == "user" else "Assistant"
            formatted.append(f"{role}: {msg.content}")
        
        return "\n".join(reversed(formatted))
    
    def build_prompt(
        self,
        query: str,
        context: List[Dict[str, Any]],
        chat_history: str,
        user_context: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Build the prompt for the LLM.
        
        Args:
            query: User's query
            context: Retrieved textbook context
            chat_history: Formatted chat history
            user_context: User's learning context (optional)
        
        Returns:
            Complete prompt for the LLM
        """
        # Build context section
        context_text = ""
        if context:
            context_text = "Relevant textbook information:\n\n"
            for i, segment in enumerate(context, 1):
                context_text += f"[{i}] From '{segment['chapter_title']}' in {segment['module_name']}:\n"
                context_text += f"    {segment['text']}\n\n"
        else:
            context_text = "No relevant textbook information found.\n\n"
        
        # Build user context section
        user_context_text = ""
        if user_context:
            user_context_text = f"\nUser's current module: {user_context.get('current_module', 'Not specified')}\n"
            user_context_text += f"Preferred detail level: {user_context.get('preferred_detail_level', 'intermediate')}\n\n"
        
        # Build complete prompt
        prompt = f"""You are an AI teaching assistant for the "Physical AI & Humanoid Robotics" textbook. 
Your role is to help students learn by providing accurate answers based SOLELY on the textbook content.

{user_context_text}
{context_text}
Previous conversation:
{chat_history}

Current question: {query}

Instructions:
1. Answer the question using ONLY the textbook context provided above
2. If the context doesn't contain the answer, say "I don't have information about that in the textbook"
3. Cite the chapter and module when referencing information
4. Keep explanations clear and educational
5. If the student seems confused, break down complex concepts
6. Match the response detail level to the student's preferred level

Your response:"""
        
        return prompt
    
    def generate_response(self, prompt: str) -> str:
        """
        Generate response using Gemini API.
        
        Args:
            prompt: Complete prompt
        
        Returns:
            Generated response text
        """
        url = f"{GEMINI_API_URL}?key={GEMINI_API_KEY}"
        
        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": prompt
                        }
                    ]
                }
            ],
            "generationConfig": {
                "temperature": 0.7,
                "topK": 40,
                "topP": 0.95,
                "maxOutputTokens": 1024,
            }
        }
        
        headers = {
            "Content-Type": "application/json"
        }
        
        response = requests.post(url, headers=headers, json=payload, timeout=60)
        
        if response.status_code != 200:
            raise Exception(
                f"Gemini API error: {response.status_code} - {response.text}"
            )
        
        result = response.json()
        
        try:
            response_text = result["candidates"][0]["content"]["parts"][0]["text"]
            return response_text
        except (KeyError, IndexError) as e:
            raise Exception(f"Failed to parse Gemini API response: {e}")
    
    def chat(
        self,
        user_id: int,
        message: str,
        session_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Process a chat message using RAG.
        
        Args:
            user_id: User ID
            message: User's message
            session_id: Optional session identifier
        
        Returns:
            Dict with response and metadata
        """
        from crud_users import get_user_context, get_user_by_id
        
        # Verify user exists
        user = get_user_by_id(self.db, user_id)
        if not user:
            raise ValueError(f"User {user_id} not found")
        
        # Retrieve context from Qdrant
        context = self.retrieve_context(message, limit=5)
        
        # Get recent chat history
        chat_history_msgs = get_recent_chat_history(
            self.db,
            user_id=user_id,
            session_id=session_id,
            limit=10
        )
        chat_history = self.format_chat_history(chat_history_msgs)
        
        # Get user context
        user_ctx = get_user_context(self.db, user_id)
        user_context_dict = None
        if user_ctx:
            user_context_dict = {
                "current_module": user_ctx.current_module,
                "preferred_detail_level": user_ctx.preferred_detail_level
            }
        
        # Build prompt
        prompt = self.build_prompt(
            query=message,
            context=context,
            chat_history=chat_history,
            user_context=user_context_dict
        )
        
        # Generate response
        response_text = self.generate_response(prompt)
        
        return {
            "response": response_text,
            "context_used": len(context) > 0,
            "context_count": len(context),
            "sources": [
                {
                    "chapter": seg["chapter_title"],
                    "module": seg["module_name"],
                    "score": seg["score"]
                }
                for seg in context
            ]
        }


# Convenience function for quick RAG chat
def rag_chat(
    db: Session,
    qdrant_client: QdrantClient,
    user_id: int,
    message: str,
    session_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Quick RAG chat function.
    
    Args:
        db: Database session
        qdrant_client: Qdrant client
        user_id: User ID
        message: User's message
        session_id: Session identifier (optional)
    
    Returns:
        Response dict with answer and metadata
    """
    service = RAGService(db, qdrant_client)
    return service.chat(user_id, message, session_id)
