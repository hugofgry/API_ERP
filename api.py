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


class SendRevoke(BaseModel):
    token: str



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



# Endpoint protégé par un jeton
@app.get("/products")
async def get_product(token_data: TokenData = Depends(secure.verify_jwt_token)):
    url = "https://615f5fb4f7254d0017068109.mockapi.io/api/v1/products"
    data = get_external_api_data(url)
    return data


@app.get("/products/{product_id}")
async def get_product_by_id(product_id: int, token_data: TokenData = Depends(secure.verify_jwt_token)):
    url = f"https://615f5fb4f7254d0017068109.mockapi.io/api/v1/products/{product_id}"
    data = get_external_api_data(url)
    return data


@app.get("/validate-token")
async def validate_token(authorization: str = Header(...),token_data: TokenData = Depends(secure.verify_jwt_token)):

    # Vérifiez si le jeton est révoqué
    print(token_data.sub)
    revoked_token = db.check_revoked_token(token_data.sub)
    if revoked_token:
        raise HTTPException(status_code=401, detail="Token has been revoked")

    return {"token": authorization.split(" ")[1]}


@app.get("/products/search/{name}")
async def get_product_by(name: Optional[str] = None, token_data: TokenData = Depends(secure.verify_jwt_token)):
    url = f"https://615f5fb4f7254d0017068109.mockapi.io/api/v1/products/"
    data = get_external_api_data(url)
    items = []
    if name is not None:
        for element in data:
            if element["name"] == name: items.append(element)

    return items


@app.get("/products/searchP/{price}")
async def get_product_by(price: Optional[str] = None, token_data: TokenData = Depends(secure.verify_jwt_token)):
    url = f"https://615f5fb4f7254d0017068109.mockapi.io/api/v1/products/"
    data = get_external_api_data(url)
    itemsP = []

    if price is not None:
        for element in data:
            if element["details"]["price"] == price:
                itemsP.append(element)

    return itemsP



@app.post("/send_qr")
async def send_qr(request: SendQRRequest):
    pwd_in_db = db.get_user_pwd(request.username)[0]

    # Vérifier que les informations d'identification sont valides
    if not secure.verify_pwd(request.pwd, pwd_in_db):
        raise HTTPException(status_code=401, detail="Nom d'utilisateur ou mot de passe incorrect")
    else:
        token = secure.generate_token(request.username)
        # Stocker le jeton dans la db
        db.add_user_token(request.username, token)

        qr = qr_code.create_qr_code(token)
        mail.send_email(qr, f"{request.username}")

    return "Email sent"

@app.post("/revoke_token")
async def revoke_token(request: SendRevoke):
    token = request.token
    try:
        db.revoke_token(token)
        return f"token {token} revoked"
    except:
        return "Erreur lors de la révocation du token"




