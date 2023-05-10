import pytest
import httpx

BASE_URL = "http://127.0.0.1:8080"


def test_read_root():
    with httpx.Client() as client:
        response = client.get(f"{BASE_URL}/")
        assert response.status_code == 200
        assert response.json() == {"Hello": "World"}


def test_get_products():
    # Ajoutez un jeton JWT valide à la place de "your_valid_jwt_token_here"
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJwaWVycmVzaW1wbG9uOTc0QGdtYWlsLmNvbSIsImV4cCI6MTY4NDk2ODExNn0.3h2-FqcRpqKDXpULRCUocSru5pjCQtt0q5CsQS8RfK8"
    with httpx.Client() as client:
        response = client.get(f"{BASE_URL}/products", headers={"Authorization": f"Bearer {token}"})
        assert response.status_code == 200
        assert isinstance(response.json(), list)


def test_get_product_by_id():
    # Ajoutez un jeton JWT valide à la place de "your_valid_jwt_token_here"
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJwaWVycmVzaW1wbG9uOTc0QGdtYWlsLmNvbSIsImV4cCI6MTY4NDk2ODExNn0.3h2-FqcRpqKDXpULRCUocSru5pjCQtt0q5CsQS8RfK8"
    product_id = 1
    with httpx.Client() as client:
        response = client.get(f"{BASE_URL}/products/{product_id}", headers={"Authorization": f"Bearer {token}"})
        assert response.status_code == 200
        assert "name" in response.json()
        assert "details" in response.json()
