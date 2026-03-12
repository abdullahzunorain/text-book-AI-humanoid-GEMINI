"""
Qdrant collection initialization script.
"""
import sys
import os

# Add src to path if running directly
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from src.services.vector_store import get_qdrant_client, init_collection

def main():
    print("⏳ Initializing Qdrant collection...")
    client = get_qdrant_client()
    
    if not client:
        print("❌ Could not connect to Qdrant. Check your QDRANT_URL and QDRANT_API_KEY.")
        sys.exit(1)
        
    success, message = init_collection(client)
    
    if success:
        print(f"✅ {message}")
    else:
        print(f"❌ {message}")
        sys.exit(1)

if __name__ == "__main__":
    main()
