"""
RAG (Retrieval-Augmented Generation) service for generating AI responses.
Combines textbook context from Qdrant with chat history from Neon.
Uses the OpenAI SDK with Gemini model.
"""
from sqlalchemy.orm import Session
from qdrant_client import QdrantClient
from typing import List, Dict, Any, Optional
import os
from dotenv import load_dotenv
from openai import OpenAI

from crud_vectors import search_textbook_content
from crud_messages import get_recent_chat_history

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

class RAGService:
    """
    Service for generating RAG-based responses.
    """
    
    def __init__(self, db: Session, qdrant_client: QdrantClient):
        """
        Initialize RAG service.
        """
        self.db = db
        self.qdrant_client = qdrant_client
        
        if not GEMINI_API_KEY:
            raise ValueError(
                "GEMINI_API_KEY environment variable is not set. "
                "Please set it in your .env file."
            )
            
        self.client = OpenAI(
            api_key=GEMINI_API_KEY,
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
        )
    
    def retrieve_context(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Retrieve relevant textbook context for a query.
        """
        return search_textbook_content(
            client=self.qdrant_client,
            query=query,
            limit=limit,
            score_threshold=0.4
        )
    
    def format_chat_history(self, messages: List) -> List[Dict[str, str]]:
        """
        Format chat history into OpenAI message format.
        """
        formatted = []
        for msg in reversed(messages[:10]):
            role = "user" if msg.role == "user" else "assistant"
            formatted.append({"role": role, "content": msg.content})
        return formatted
    
    def chat(
        self,
        user_id: int,
        message: str,
        session_id: Optional[str] = None,
        selected_text: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Process a chat message using RAG or selected text.
        """
        from crud_users import get_user_context, get_user_by_id
        
        user = get_user_by_id(self.db, user_id)
        if not user:
            raise ValueError(f"User {user_id} not found")
        
        user_ctx = get_user_context(self.db, user_id)
        user_context_str = ""
        if user_ctx:
            user_context_str = f"User's current module: {user_ctx.current_module}\nPreferred detail level: {user_ctx.preferred_detail_level}\n"
        
        context = []
        sources = []
        system_prompt = "You are an AI teaching assistant for the 'Physical AI & Humanoid Robotics' textbook."
        
        if selected_text:
            system_prompt += f"""
The student has selected the following text from the textbook:
\"\"\"
{selected_text}
\"\"\"
{user_context_str}
Instructions:
1. Answer the student's question based ONLY on the selected text above.
2. Do not use outside knowledge. If the text does not contain the answer, explicitly state that the selected text doesn't provide enough information.
"""
            context_used = True
        else:
            context = self.retrieve_context(message, limit=5)
            context_used = len(context) > 0
            
            context_text = "No relevant textbook information found.\n"
            if context_used:
                sources = [
                    {"chapter": seg["chapter_title"], "module": seg["module_name"], "score": seg["score"]}
                    for seg in context
                ]
                context_text = "Relevant textbook information:\n\n"
                for i, segment in enumerate(context, 1):
                    context_text += f"[{i}] From '{segment['chapter_title']}' in {segment['module_name']}:\n"
                    context_text += f"    {segment['text']}\n\n"
            
            system_prompt += f"""
{user_context_str}
{context_text}
Instructions:
1. Answer the question using ONLY the textbook context provided above.
2. If the context doesn't contain the answer, say "I don't have information about that in the textbook".
3. Cite the chapter and module when referencing information.
4. Keep explanations clear and educational.
"""

        chat_history_msgs = get_recent_chat_history(self.db, user_id=user_id, session_id=session_id, limit=10)
        
        messages = [{"role": "system", "content": system_prompt}]
        messages.extend(self.format_chat_history(chat_history_msgs))
        messages.append({"role": "user", "content": message})
        
        response = self.client.chat.completions.create(
            model="gemini-2.0-flash",
            messages=messages,
            temperature=0.7,
            max_tokens=1024
        )
        
        return {
            "response": response.choices[0].message.content,
            "context_used": context_used,
            "context_count": len(context) if not selected_text else 1,
            "sources": sources
        }

    def personalize_content(self, user_id: int, content: str) -> str:
        """Personalize content based on user's background."""
        from crud_users import get_user_by_id
        user = get_user_by_id(self.db, user_id)
        
        hardware = user.hardware_background if user else "None"
        software = user.software_background if user else "None"
            
        system_prompt = f"""
You are an expert AI textbook author. Rewrite the provided textbook content to make it more personalized for a reader with this background:
- Hardware: {hardware}
- Software: {software}
"""
        user_msg = f"Personalize the following content while maintaining core concepts and structure:\n\n{content}"
        
        response = self.client.chat.completions.create(
            model="gemini-2.0-flash",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_msg}
            ],
            temperature=0.7,
            max_tokens=2048
        )
        return response.choices[0].message.content

    def translate_content(self, content: str) -> str:
        """Translate content to Urdu."""
        system_prompt = "You are an expert translator. Translate the following technical textbook content into Urdu. Maintain the formatting, markdown tags, and technical terms where appropriate."
        
        response = self.client.chat.completions.create(
            model="gemini-2.0-flash",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Translate this content:\n\n{content}"}
            ],
            temperature=0.3,
            max_tokens=4000
        )
        return response.choices[0].message.content

def rag_chat(db: Session, qdrant_client: QdrantClient, user_id: int, message: str, session_id: Optional[str] = None, selected_text: Optional[str] = None) -> Dict[str, Any]:
    service = RAGService(db, qdrant_client)
    return service.chat(user_id, message, session_id, selected_text)
