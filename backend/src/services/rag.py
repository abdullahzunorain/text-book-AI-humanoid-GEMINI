"""
RAG (Retrieval-Augmented Generation) service for generating AI responses.
Combines textbook context from Qdrant with chat history from Neon.
Uses the OpenAI SDK with Gemini model.
"""
from sqlalchemy.ext.asyncio import AsyncSession
from qdrant_client import QdrantClient
from typing import List, Dict, Any, Optional
import os
from dotenv import load_dotenv
from openai import OpenAI

from src.db.crud_vectors import search_textbook_content
from src.db.crud_messages import get_recent_chat_history, create_message
from src.db.crud_users import get_user_by_id, get_user_context

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


class RAGService:
    """
    Service for generating RAG-based responses.
    """

    def __init__(self, db: AsyncSession, qdrant_client: Optional[QdrantClient]):
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
        """Retrieve relevant textbook context for a query."""
        if not self.qdrant_client:
            return []
        return search_textbook_content(
            client=self.qdrant_client,
            query=query,
            limit=limit,
            score_threshold=0.4
        )

    def format_chat_history(self, messages: List) -> List[Dict[str, str]]:
        """Format chat history into OpenAI message format."""
        formatted = []
        for msg in reversed(messages[:10]):
            role = "user" if msg.role == "user" else "assistant"
            formatted.append({"role": role, "content": msg.content})
        return formatted

    async def chat(
        self,
        user_id: int,
        message: str,
        session_id: Optional[str] = None,
        selected_text: Optional[str] = None
    ) -> Dict[str, Any]:
        """Process a chat message using RAG or selected text."""
        user = await get_user_by_id(self.db, user_id)
        if not user:
            raise ValueError(f"User {user_id} not found")

        user_ctx = await get_user_context(self.db, user_id)
        user_context_str = ""
        if user_ctx:
            user_context_str = (
                f"User's current module: {user_ctx.current_module}\n"
                f"Preferred detail level: {user_ctx.preferred_detail_level}\n"
            )

        context = []
        sources = []
        system_prompt = (
            "You are an AI teaching assistant for the "
            "'Physical AI & Humanoid Robotics' textbook."
        )

        # Truncate selected_text to 3000 chars to guard context window
        if selected_text and len(selected_text) > 3000:
            selected_text = selected_text[:3000]

        if selected_text:
            system_prompt += f"""
The student has selected the following text from the textbook:
\"\"\"
{selected_text}
\"\"\"
{user_context_str}
Instructions:
1. Answer the student's question based ONLY on the selected text above.
2. Do not use outside knowledge. If the text does not contain the answer, \
explicitly state that the selected text doesn't provide enough information.
"""
            context_used = True
        else:
            context = self.retrieve_context(message, limit=5)
            context_used = len(context) > 0

            context_text = "No relevant textbook information found.\n"
            if context_used:
                sources = [
                    {
                        "chapter": seg["chapter_title"],
                        "module": seg["module_name"],
                        "score": seg["score"]
                    }
                    for seg in context
                ]
                context_text = "Relevant textbook information:\n\n"
                for i, segment in enumerate(context, 1):
                    context_text += (
                        f"[{i}] From '{segment['chapter_title']}' "
                        f"in {segment['module_name']}:\n"
                        f"    {segment['text']}\n\n"
                    )

            system_prompt += f"""
{user_context_str}
{context_text}
Instructions:
1. Answer the question using ONLY the textbook context provided above.
2. If the context doesn't contain the answer, say \
"I don't have information about that in the textbook".
3. Cite the chapter and module when referencing information.
4. Keep explanations clear and educational.
"""

        chat_history_msgs = await get_recent_chat_history(
            self.db, user_id=user_id, session_id=session_id, limit=10
        )

        messages_list = [{"role": "system", "content": system_prompt}]
        messages_list.extend(self.format_chat_history(chat_history_msgs))
        messages_list.append({"role": "user", "content": message})

        response = self.client.chat.completions.create(
            model=os.getenv("GEMINI_MODEL", "gemini-2.0-flash"),
            messages=messages_list,
            temperature=0.7,
            max_tokens=1024
        )

        ai_response = response.choices[0].message.content

        # Persist messages
        await create_message(self.db, user_id=user_id, role="user",
                             content=message, session_id=session_id)
        await create_message(self.db, user_id=user_id, role="assistant",
                             content=ai_response, session_id=session_id)

        return {
            "response": ai_response,
            "context_used": context_used,
            "context_count": len(context) if not selected_text else 1,
            "sources": sources,
            "session_id": session_id,
        }

    async def personalize_content(self, user_id: int, content: str) -> str:
        """Personalize content based on user's background."""
        user = await get_user_by_id(self.db, user_id)

        hardware = user.hardware_background if user else "None"
        software = user.software_background if user else "None"

        system_prompt = (
            "You are an expert AI textbook author. Rewrite the provided textbook "
            "content to make it more personalized for a reader with this background:\n"
            f"- Hardware: {hardware}\n"
            f"- Software: {software}"
        )
        user_msg = (
            "Personalize the following content while maintaining core concepts "
            f"and structure:\n\n{content}"
        )

        response = self.client.chat.completions.create(
            model=os.getenv("GEMINI_MODEL", "gemini-2.0-flash"),
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_msg}
            ],
            temperature=0.7,
            max_tokens=2048
        )
        return response.choices[0].message.content

    async def translate_content(self, content: str) -> str:
        """Translate content to Urdu."""
        system_prompt = (
            "You are an expert translator. Translate the following technical textbook "
            "content into Urdu. Maintain the formatting, markdown tags, and technical "
            "terms where appropriate."
        )

        response = self.client.chat.completions.create(
            model=os.getenv("GEMINI_MODEL", "gemini-2.0-flash"),
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Translate this content:\n\n{content}"}
            ],
            temperature=0.3,
            max_tokens=4000
        )
        return response.choices[0].message.content
