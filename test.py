from fastapi.testclient import TestClient
import pytest
import httpx
from main import app  # Assurez-vous d'importer le bon fichier
from pydantic import BaseModel
import secure

client = TestClient(app)

class MockResponse:
    def __init__(self, status_code, json_data):
        self.status_code = status_code
        self._json_data = json_data

    def json(self):
        return self._json_data

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}

def test_send_qr_invalid_credentials(monkeypatch):
    class SendQRRequest(BaseModel):
        username: str
        pwd: str

    def mock_get_user_pwd(username):
        return ("hashed_password",)

    monkeypatch.setattr("main.db.get_user_pwd", mock_get_user_pwd)
    monkeypatch.setattr("main.secure.verify_pwd", lambda pwd, hashed: False)

    response = client.post("/send_qr", json={"username": "user", "pwd": "invalid_pwd"})
    assert response.status_code == 401
    assert response.json() == {"detail": "Nom d'utilisateur ou mot de passe incorrect"}

@pytest.mark.asyncio
async def test_get_product(monkeypatch):
    async def mock_verify_jwt_token(token_data):
        return {"username": "user"}

    async def mock_get_external_api_data(url):
        return [{"id": "1", "name": "Product 1", "price": "50"}]

    monkeypatch.setattr("main.secure.verify_jwt_token", mock_verify_jwt_token)
    monkeypatch.setattr("main.get_external_api_data", mock_get_external_api_data)

    async with httpx.AsyncClient(app=app) as ac:
        response = await ac.get("/products")
    assert response.status_code == 200
    assert response.json() == [{"id": "1", "name": "Product 1", "price": "50"}]

@pytest.mark.asyncio
async def test_validate_token(monkeypatch):
    def mock_get_user_by_token(token):
        return {"username": "user"}

    monkeypatch.setattr("main.db.get_user_by_token", mock_get_user_by_token)

    token = secure.generate_token("user")
    headers = {"Authorization": f"Bearer {token}"}
    async with httpx.AsyncClient(app=app) as ac:
        response = await ac.get("/validate-token", headers=headers)
    assert response.status_code == 200
    assert response.json() == {"token": token}


import json

# ... (imports et tests précédents)

# Ajoutez cette fonction pour simuler une réponse d'API externe
def create_mock_product_data(product_id=None):
    data = [
        {"id": "1", "name": "Product 1", "price": "50"},
        {"id": "2", "name": "Product 2", "price": "75"},
        {"id": "3", "name": "Product 3", "price": "100"},
    ]
    if product_id:
        return [item for item in data if item["id"] == product_id][0]
    return data


@pytest.mark.asyncio
async def test_get_product_by_id(monkeypatch):
    async def mock_verify_jwt_token(token_data):
        return {"username": "user"}

    def mock_get_external_api_data(url):
        product_id = url.split("/")[-1]
        return create_mock_product_data(product_id)

    monkeypatch.setattr("main.secure.verify_jwt_token", mock_verify_jwt_token)
    monkeypatch.setattr("main.get_external_api_data", mock_get_external_api_data)

    async with httpx.AsyncClient(app=app) as ac:
        response = await ac.get("/products/1")
    assert response.status_code == 200
    assert response.json() == {"id": "1", "name": "Product 1", "price": "50"}


@pytest.mark.asyncio
async def test_get_product_by_name(monkeypatch):
    async def mock_verify_jwt_token(token_data):
        return {"username": "user"}

    def mock_get_external_api_data(url):
        return create_mock_product_data()

    monkeypatch.setattr("main.secure.verify_jwt_token", mock_verify_jwt_token)
    monkeypatch.setattr("main.get_external_api_data", mock_get_external_api_data)

    async with httpx.AsyncClient(app=app) as ac:
        response = await ac.get("/products/search", params={"name": "Product 2"})
    assert response.status_code == 200
    assert response.json() == [{"id": "2", "name": "Product 2", "price": "75"}]


@pytest.mark.asyncio
async def test_get_product_by_price(monkeypatch):
    async def mock_verify_jwt_token(token_data):
        return {"username": "user"}

    def mock_get_external_api_data(url):
        return create_mock_product_data()

    monkeypatch.setattr("main.secure.verify_jwt_token", mock_verify_jwt_token)
    monkeypatch.setattr("main.get_external_api_data", mock_get_external_api_data)

    async with httpx.AsyncClient(app=app) as ac:
        response = await ac.get("/products/search", params={"price": "100"})
    assert response.status_code == 200
    assert response.json() == [{"id": "3", "name": "Product 3", "price": "100"}]

# Test de l'échec de l'authentification de jeton
@pytest.mark.asyncio
async def test_validate_token_invalid_token(monkeypatch):
    def mock_get_user_by_token(token):
        return None

    monkeypatch.setattr("main.db.get_user_by_token", mock_get_user_by_token)

    invalid_token = "invalid_token"
    headers = {"Authorization": f"Bearer {invalid_token}"}
    async with httpx.AsyncClient(app=app) as ac:
        response = await ac.get("/validate-token", headers=headers)
    assert response.status