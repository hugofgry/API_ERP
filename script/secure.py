import datetime
import db
from argon2 import PasswordHasher
import jwt as pyjwt


TOKEN_EXPIRATION_TIME = datetime.timedelta(days=14)


def generate_token(username: str, pass_phrase: str) -> str:
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




