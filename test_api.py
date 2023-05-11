import httpx
import pytest
from fastapi.testclient import TestClient


API_BASE_URL = "http://127.0.0.1:8080"

def test_read_root():
    response = httpx.get(f"{API_BASE_URL}/")
    assert response.status_code == 200


def test_validate_token_invalid():
    response = httpx.get(f"{API_BASE_URL}/validate-token", headers={"Authorization": "Bearer invalid_token"})
    assert response.status_code == 401


def test_send_qr_invalid_credentials():
    response = httpx.post(f"{API_BASE_URL}/send_qr", json={"username": "invalid_user", "pwd": "invalid_password"})
    assert response.status_code == 401


def test_revoke_token_invalid():
    response = httpx.post(f"{API_BASE_URL}/revoke_token", json={"token": "invalid_token"})
    assert response.status_code == 200

