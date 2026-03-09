# Ingest Textbook Content

Autonomous skill to run the RAG ingestion pipeline and verify Qdrant vector store.

## Steps

1. Change to the backend directory: `cd backend`
2. Verify the `.env` file exists with `QDRANT_URL`, `QDRANT_API_KEY`, and `GEMINI_API_KEY`
3. Run the Qdrant collection initialization: `uv run python scripts/init_qdrant.py`
4. Run the textbook ingestion script: `uv run python scripts/ingest_textbook.py`
5. Verify the ingestion by checking Qdrant collection stats — confirm chunk count > 0
6. Report: total chunks ingested, chunks per module, collection dimensions, and any errors

## Expected Output

```
Ingestion complete:
- Total chunks: <N>
- Module 1 (ROS 2): <n> chunks
- Module 2 (Digital Twin): <n> chunks
- Module 3 (NVIDIA Isaac): <n> chunks
- Module 4 (VLA): <n> chunks
- Vector dimensions: 768
- Collection: textbook_chunks
```

## Error Handling

- If `GEMINI_API_KEY` is missing, report and stop
- If `QDRANT_URL` is missing, report and stop
- If ingestion fails partway, report which module failed and how many chunks succeeded
