import datetime
import db
import argon2
import jwt as pyjwt
from pydantic import BaseModel
from fastapi import FastAPI, Depends, HTTPException, Header
import os
import secrets
from jwt.exceptions import ExpiredSignatureError, InvalidSignatureError


TOKEN_EXPIRATION_TIME = datetime.timedelta(days=14)

pass_phrase = os.environ.get("TOKEN_API_CRM")
if not isinstance(pass_phrase, str):
        pass_phrase = str(pass_phrase)



class TokenData(BaseModel):
    sub: str

def generate_token(username: str) -> str:
    # Définir la date d'expiration du jeton
    expiration = datetime.datetime.utcnow() + TOKEN_EXPIRATION_TIME

    # Créer la charge utile pour le jeton JWT (nous incluons le nom d'utilisateur et la date d'expiration)
    payload = {"sub": username, "exp": expiration}

    # Créer le jeton JWT en signant la charge utile avec la clé secrète
    token = pyjwt.encode(payload, pass_phrase, algorithm="HS256")

    # Stocker le jeton dans la db
    db.add_user_token(username,token)

    # Retourner le jeton en tant que chaîne de caractères
    return token


def verify_jwt_token(authorization: str = Header(...)) -> TokenData:
    try:
        token = authorization.split(" ")[1]
        payload = pyjwt.decode(token, pass_phrase, algorithms="HS256")
        # Reste de la fonction
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid JWT token")
        token_data = TokenData(sub=user_id)
        return token_data
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="JWT token has expired")
    except InvalidSignatureError:
        raise HTTPException(status_code=401, detail="Invalid JWT signature")
    except pyjwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid JWT token")
    return token_datax

def hash_pwd(pwd: str) -> str:
    ph = argon2.PasswordHasher()
    return ph.hash(pwd)


def verify_pwd(user_pwd: str, hashed_pwd_from_db: str) -> bool:
    ph = argon2.PasswordHasher()
    try:
        ph.verify(hashed_pwd_from_db, user_pwd)
        return True
    except:
        return False




