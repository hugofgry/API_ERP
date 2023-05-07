from argon2 import PasswordHasher
import jwt



def generate_token(username: str) -> str:
    # Définir la date d'expiration du jeton
    expiration = datetime.utcnow() + TOKEN_EXPIRATION_TIME

    # Créer la charge utile pour le jeton JWT (nous incluons le nom d'utilisateur et la date d'expiration)
    payload = {"sub": username, "exp": expiration}

    # Créer le jeton JWT en signant la charge utile avec la clé secrète
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

    # Retourner le jeton en tant que chaîne de caractères
    return token


def hash_pwd(pwd: str) -> str:
    ph = PasswordHasher()
    return ph.hash(pwd)


def verify_pwd(user_pwd: str, hashed_pwd: str) -> bool:
    hashed_user_password = hash_pwd(user_pwd)
    try:
        ph.verify(hashed_user_password, hashed_pwd)
        return True
    except:
        return False




