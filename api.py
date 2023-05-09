from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import db
import secure
from secure import TokenData
import qr_code
import mail
import requests
from fastapi import FastAPI, Depends, HTTPException, Header
from typing import Optional

app = FastAPI()
security = HTTPBearer()


class SendQRRequest(BaseModel):
    username: str
    pwd: str


def get_external_api_data(url: str):
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        raise HTTPException(status_code=500, detail="Unable to fetch data from external API")


@app.get("/")
def read_root():
    return {"Hello": "World"}



@app.post("/send_qr")
async def send_qr(request: SendQRRequest):
    pwd_in_db = db.get_user_pwd(request.username)[0]

    # Vérifier que les informations d'identification sont valides
    if not secure.verify_pwd(request.pwd, pwd_in_db):
        raise HTTPException(status_code=401, detail="Nom d'utilisateur ou mot de passe incorrect")
    else:
        token = secure.generate_token(request.username)
        qr = qr_code.create_qr_code(token)
        mail.send_email(qr, f"{request.username}")

    return "Email sent"

# Endpoint protégé par un jeton
@app.get("/products")
async def get_product(token_data: TokenData = Depends(secure.verify_jwt_token)):
    url = "https://615f5fb4f7254d0017068109.mockapi.io/api/v1/products"
    data = get_external_api_data(url)
    return data

@app.get("/validate-token")
async def validate_token(authorization: str = Header(...)):
    try:
        scheme, token = authorization.split(" ")
        if scheme.lower() != "bearer":
            raise HTTPException(status_code=401, detail="Invalid authentication scheme.")
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid authorization header format.")
    user = db.get_user_by_token(token)
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid token.")
    return {"token": token}

@app.get("/products/{product_id}")
async def get_product_by_id(product_id: int, token_data: TokenData = Depends(secure.verify_jwt_token)):
    url = f"https://615f5fb4f7254d0017068109.mockapi.io/api/v1/products/{product_id}"
    data = get_external_api_data(url)
    return data


@app.get("/products/search/{name}{price}")
async def get_product_by(name: Optional[str] = None, price: Optional[str] = None, token_data: TokenData = Depends(secure.verify_jwt_token)):
    url = f"https://615f5fb4f7254d0017068109.mockapi.io/api/v1/products/"
    data = get_external_api_data(url)

    items = []

    if name is not None:
        for element in data:
            if element["name"] == name:
                items.append(element)

    elif price is not None:
        for element in data:
            if element["price"] == price:
                items.append(element)

    return items

