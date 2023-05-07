from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import datetime, timedelta
import jwt as pyjwt
import db
import secure
import qr_code
import mail

app = FastAPI()
security = HTTPBearer()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/send_qr")
async def send_qr(username,pwd,user_passphrase):

    pwd_in_db = db.get_user_pwd(username)[0]
    print(pwd_in_db)

    # Vérifier que les informations d'identification sont valides
    if not secure.verify_pwd(pwd,pwd_in_db) :
        raise HTTPException(status_code=401, detail="Nom d'utilisateur ou mot de passe incorrect")

    else:
        token = secure.generate_token(username,user_passphrase)
        qr = qr_code.create_qr_code(token)
        mail.send_email(qr,"lamrani002@gmail.com")

    return "Email sent"


# Endpoint protégé par un jeton
@app.get("/data")
async def protected_data(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        # Extraire le jeton JWT de l'en-tête d'autorisation
        token = credentials.credentials

        # Décoder et vérifier le jeton JWT
        payload = pyjwt.decode(token, SECRET_KEY, algorithms=["HS256"])

        # Vérifier que le jeton n'a pas expiré
        expiration = datetime.fromtimestamp(payload["exp"])
        if datetime.utcnow() > expiration:
            raise HTTPException(status_code=401, detail="Le jeton d'authentification a expiré")

        # Renvoyer les données protégées
        return {"data": "Ceci sont des données protégées!"}

    except pyjwt.JWTError:
        raise HTTPException(status_code=401, detail="Jeton d'authentification invalide")




