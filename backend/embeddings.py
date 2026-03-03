"""
Embeddings generation using Gemini API.
"""
import os
from dotenv import load_dotenv
from typing import List, Union
import requests
import json

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_EMBEDDINGS_URL = "https://generativelanguage.googleapis.com/v1beta/models/text-embedding-004:embedContent"


def get_embedding(text: str) -> List[float]:
    """
    Get embedding vector for a single text using Gemini API.
    
    Args:
        text: Text to embed
    
    Returns:
        List of floats representing the embedding vector
    
    Raises:
        ValueError: If API key is not set
        Exception: If API request fails
    """
    if not GEMINI_API_KEY:
        raise ValueError(
            "GEMINI_API_KEY environment variable is not set. "
            "Please set it in your .env file."
        )
    
    url = f"{GEMINI_EMBEDDINGS_URL}?key={GEMINI_API_KEY}"
    
    payload = {
        "model": "text-embedding-004",
        "content": {
            "parts": [
                {
                    "text": text
                }
            ]
        }
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    response = requests.post(url, headers=headers, json=payload, timeout=30)
    
    if response.status_code != 200:
        raise Exception(
            f"Gemini API error: {response.status_code} - {response.text}"
        )
    
    result = response.json()
    embedding = result.get("embedding", {}).get("values", [])
    
    if not embedding:
        raise Exception("Empty embedding returned from Gemini API")
    
    return embedding


def get_embeddings(texts: List[str]) -> List[List[float]]:
    """
    Get embedding vectors for multiple texts.
    
    Args:
        texts: List of texts to embed
    
    Returns:
        List of embedding vectors
    """
    embeddings = []
    for text in texts:
        embedding = get_embedding(text)
        embeddings.append(embedding)
    return embeddings


def get_embedding_dimension() -> int:
    """
    Get the dimension of embeddings produced by the model.
    
    Returns:
        Dimension size (768 for text-embedding-004)
    """
    # Gemini text-embedding-004 produces 768-dimensional vectors
    return 768


# Test function
if __name__ == "__main__":
    test_text = "This is a test sentence about ROS 2 and robotics."
    
    try:
        embedding = get_embedding(test_text)
        print(f"✅ Successfully generated embedding")
        print(f"   Dimension: {len(embedding)}")
        print(f"   First 10 values: {embedding[:10]}")
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\nMake sure you have set GEMINI_API_KEY in your .env file")
