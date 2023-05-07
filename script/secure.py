import datetime
import db
from argon2 import PasswordHasher
import jwt as pyjwt
from pydantic import BaseModel
from fastapi import HTTPException




TOKEN_EXPIRATION_TIME = datetime.timedelta(days=14)
pass_phrase = "jesuisunefougere974"

class TokenData(BaseModel):
    sub: str

def generate_token(username: str) -> str:
    # Définir la date d'expiration du jeton
    expiration = datetime.datetime.utcnow() + TOKEN_EXPIRATION_TIME

    # Créer la charge utile pour le jeton JWT (nous incluons le nom d'utilisateur et la date d'expiration)
    payload = {"sub": username, "exp": expiration}

    # Créer le jeton JWT en signant la charge utile avec la clé secrète
    token = pyjwt.encode(payload, pass_phrase, algorithm="HS256")
    print("token généré pour l'user :" + username)

    # Stocker le jeton dans la db
    db.add_user_token(username,token)
    print("token ajouté dans la db pour l'user :" + username)

    # Retourner le jeton en tant que chaîne de caractères
    return token

def verify_jwt_token(token: str) -> TokenData:
    try:
        payload = pyjwt.decode(token, pass_phrase, algorithms="HS256")
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid JWT token")
        token_data = TokenData(sub=user_id)
        return token_data
    except pyjwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid JWT token")


def hash_pwd(pwd: str) -> str:
    ph = PasswordHasher()
    return ph.hash(pwd)


def verify_pwd(user_pwd: str, hashed_pwd_from_db: str) -> bool:
    ph = PasswordHasher()
    try:
        ph.verify(hashed_pwd_from_db, user_pwd)
        return True
    except:
        return False




