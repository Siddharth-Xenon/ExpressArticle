import pytest
from httpx import AsyncClient
from fastapi import FastAPI, Depends, HTTPException, status
from app.dependencies import auth

app = FastAPI()

# Mock endpoint to test the token verification


@app.get("/test-token")
async def test_token(current_user: str = Depends(auth.get_current_user)):
    return {"user": current_user}

# Setup for the tests


@pytest.fixture
def client():
    with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

# Test for token creation


@pytest.mark.asyncio
async def test_create_access_token():
    test_user_data = {"sub": "testuser"}
    token = auth.create_access_token(data=test_user_data)
    assert token is not None

# Test for token verification (Positive)


@pytest.mark.asyncio
async def test_verify_token(client: AsyncClient):
    test_user_data = {"sub": "testuser"}
    token = auth.create_access_token(data=test_user_data)
    headers = {"Authorization": f"Bearer {token}"}
    response = await client.get("/test-token", headers=headers)
    assert response.status_code == 200
    assert response.json()["user"] == "testuser"

# Test for token verification (Negative)


@pytest.mark.asyncio
async def test_verify_token_invalid(client: AsyncClient):
    headers = {"Authorization": "Bearer invalidtoken"}
    response = await client.get("/test-token", headers=headers)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
