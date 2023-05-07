from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import datetime, timedelta
import jwt as pyjwt
import db
import secure
from secure import TokenData
import qr_code
import mail
import requests
from fastapi import FastAPI, Depends, HTTPException


app = FastAPI()
security = HTTPBearer()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/send_qr")
async def send_qr(username,pwd):

    pwd_in_db = db.get_user_pwd(username)[0]
    print(pwd_in_db)

    # Vérifier que les informations d'identification sont valides
    if not secure.verify_pwd(pwd,pwd_in_db) :
        raise HTTPException(status_code=401, detail="Nom d'utilisateur ou mot de passe incorrect")

    else:
        token = secure.generate_token(username)
        qr = qr_code.create_qr_code(token)
        mail.send_email(qr,"lamrani002@gmail.com")

    return "Email sent"



# Endpoint protégé par un jeton
@app.get("/products")
async def get_product(token_data: TokenData = Depends(secure.verify_jwt_token)):

    url = "https://615f5fb4f7254d0017068109.mockapi.io/api/v1/products"
    response = requests.get(url)
    if response.status_code == 200:
        # Parse the JSON data from the response
        data = response.json()

    return data





