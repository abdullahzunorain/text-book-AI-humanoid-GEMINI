import pytest


@pytest.mark.asyncio
async def test_create_user(client):
    response = await client.post(
        "/users/",
        json={
            "name": "Test User",
            "email": "test@example.com",
            "hardware_background": "RTX GPU",
            "software_background": "Intermediate Python",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test User"
    assert data["email"] == "test@example.com"
    assert data["hardware_background"] == "RTX GPU"
    assert "id" in data


@pytest.mark.asyncio
async def test_get_user(client):
    # Create first
    create_resp = await client.post(
        "/users/",
        json={"name": "Jane", "email": "jane@example.com"},
    )
    user_id = create_resp.json()["id"]

    # Get
    response = await client.get(f"/users/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Jane"
    assert data["id"] == user_id


@pytest.mark.asyncio
async def test_get_user_not_found(client):
    response = await client.get("/users/99999")
    assert response.status_code == 404
