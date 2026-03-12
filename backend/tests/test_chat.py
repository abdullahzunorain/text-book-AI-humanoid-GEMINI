import pytest
from unittest.mock import patch, MagicMock


@pytest.mark.asyncio
async def test_chat_missing_fields(client):
    """POST /chat/ with missing required fields returns 422."""
    response = await client.post("/chat/", json={})
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_chat_with_mock(client):
    """POST /chat/ with mocked Gemini returns a response with sources."""
    mock_completion = MagicMock()
    mock_completion.choices = [
        MagicMock(message=MagicMock(content="ROS 2 is a robot operating system."))
    ]

    with patch("src.services.rag.RAGService.chat") as mock_chat:
        mock_chat.return_value = {
            "response": "ROS 2 is a robot operating system.",
            "context_used": True,
            "context_count": 2,
            "sources": [
                {"chapter": "Week 1", "module": "Module 1", "score": 0.92}
            ],
            "session_id": "test-session-123",
        }

        response = await client.post(
            "/chat/",
            json={
                "message": "What is ROS 2?",
                "session_id": "test-session-123",
            },
        )

    assert response.status_code == 200
    data = response.json()
    assert "ROS 2" in data["response"]
    assert data["session_id"] == "test-session-123"
    assert len(data["sources"]) >= 1


@pytest.mark.asyncio
async def test_chat_with_selected_text(client):
    """POST /chat/ with selected_text uses that as context."""
    with patch("src.services.rag.RAGService.chat") as mock_chat:
        mock_chat.return_value = {
            "response": "This selected text explains nodes.",
            "context_used": True,
            "context_count": 1,
            "sources": [],
            "session_id": "sel-session",
        }

        response = await client.post(
            "/chat/",
            json={
                "message": "Explain this",
                "session_id": "sel-session",
                "selected_text": "A ROS 2 node is a process that performs computation.",
            },
        )

    assert response.status_code == 200
    data = response.json()
    assert "response" in data
