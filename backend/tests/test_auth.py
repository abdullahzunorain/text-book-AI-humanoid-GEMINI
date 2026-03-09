import pytest


@pytest.mark.asyncio
async def test_chat_without_auth(client):
    """POST /chat/ without auth header should still work (fallback to user_id=1)."""
    from unittest.mock import patch, MagicMock

    with patch("src.services.rag.RAGService.chat") as mock_chat:
        mock_chat.return_value = {
            "response": "Test response",
            "context_used": False,
            "context_count": 0,
            "sources": [],
            "session_id": "s1",
        }
        response = await client.post(
            "/chat/",
            json={"message": "Hello", "session_id": "s1"},
        )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_chat_with_valid_auth(client):
    """POST /chat/ with valid Bearer token uses authenticated user_id."""
    from unittest.mock import patch

    # First create a user
    create_resp = await client.post(
        "/users/",
        json={"name": "Auth User", "email": "auth@test.com"},
    )
    user_id = create_resp.json()["id"]

    with patch("src.services.rag.RAGService.chat") as mock_chat:
        mock_chat.return_value = {
            "response": "Authenticated response",
            "context_used": False,
            "context_count": 0,
            "sources": [],
            "session_id": "s2",
        }
        response = await client.post(
            "/chat/",
            json={"message": "Hello", "session_id": "s2"},
            headers={"Authorization": f"Bearer {user_id}"},
        )
    assert response.status_code == 200
    data = response.json()
    assert data["response"] == "Authenticated response"


@pytest.mark.asyncio
async def test_user_lookup_by_email(client):
    """GET /users/lookup?email=... returns user profile."""
    # Create user first
    await client.post(
        "/users/",
        json={"name": "Lookup User", "email": "lookup@test.com"},
    )

    response = await client.get("/users/lookup?email=lookup@test.com")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Lookup User"
    assert data["email"] == "lookup@test.com"


@pytest.mark.asyncio
async def test_user_lookup_not_found(client):
    """GET /users/lookup?email=... returns 404 for missing user."""
    response = await client.get("/users/lookup?email=nobody@test.com")
    assert response.status_code == 404
