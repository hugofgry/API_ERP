from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import datetime, timedelta
import jwt
import db
import secure
import qr_code
import mail

app = FastAPI()
security = HTTPBearer()

@app.get("/login")
async def login():

    username = "mulder974"
    pwd =  "tiTeuf145*"
    pwd_in_db, token_in_db = db.get_user_pwd_and_token(username)


    # Vérifier que les informations d'identification sont valides
    if secure.verify_pwd(pwd,pwd_in_db) :
        raise HTTPException(status_code=401, detail="Nom d'utilisateur ou mot de passe incorrect")

    else:
        qr_code.create_qr_code(token_in_db)
        mail.send_email(qr_code)

    return "access to API ok"



