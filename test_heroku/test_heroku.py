import requests
import os

API_BASE_URL = "https://apiepsierp.herokuapp.com"
VALID_TOKEN = os.environ['TOKEN']

def test_get_products_with_valid_token_production():
    response = requests.get(
        f"{API_BASE_URL}/products",
        headers={"Authorization": f"Bearer {VALID_TOKEN}"}
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_product_by_id_with_valid_token_production():
    product_id = 3
    response = requests.get(
        f"{API_BASE_URL}/products/{product_id}",
        headers={"Authorization": f"Bearer {VALID_TOKEN}"}
    )
    assert response.status_code == 200
    assert "id" in response.json() and response.json()["id"] == str(product_id)

def test_get_product_by_name_with_valid_token_production():
    product_name = "Café de Julien Couraud"
    response = requests.get(
        f"{API_BASE_URL}/products/search/{product_name}",
        headers={"Authorization": f"Bearer {VALID_TOKEN}"}
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert all(product["name"] == product_name for product in response.json())
