"""
Embeddings generation using Google Gemini API.
"""
import os
import google.generativeai as genai
from typing import List, Union
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "models/embedding-001") # models/embedding-001 has 768 dimensions

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

def get_embedding(text: str, model: str = EMBEDDING_MODEL) -> List[float]:
    """
    Generate embedding for a single string.
    """
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY is not set")
    
    # Pre-process text to remove newlines
    text = text.replace("\n", " ")
    
    result = genai.embed_content(
        model=model,
        content=text,
        task_type="retrieval_document",
        title="Textbook Chunk"
    )
    
    return result['embedding']

def get_embeddings_batch(texts: List[str], model: str = EMBEDDING_MODEL) -> List[List[float]]:
    """
    Generate embeddings for a list of strings.
    """
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY is not set")
    
    # Pre-process texts
    processed_texts = [t.replace("\n", " ") for t in texts]
    
    result = genai.embed_content(
        model=model,
        content=processed_texts,
        task_type="retrieval_document"
    )
    
    return result['embeddings']

if __name__ == "__main__":
    # Quick test
    try:
        test_text = "Physical AI and Humanoid Robotics are exciting fields."
        embedding = get_embedding(test_text)
        print(f"✅ Embedding generated successfully")
        print(f"   Dimension: {len(embedding)}")
        print(f"   First 10 values: {embedding[:10]}")
    except Exception as e:
        print(f"❌ Error: {e}")
