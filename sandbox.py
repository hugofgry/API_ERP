import psycopg2 as psy
import db
import secure

def set_connection():
  connection = psy.connect('postgres://testneon33:dfkFh5jcr1Tw@ep-hidden-forest-997741.eu-central-1.aws.neon.tech/neondb?sslmode=require')
  connection.set_session(autocommit=True)
  cursor = connection.cursor()
  return connection, cursor


def get_user_pwd_and_token(user_name):

    connection,cursor = set_connection()
    cursor.execute("""SELECT pwd,user_token FROM Users WHERE username = %s""", (str(user_name),))
    pwd, token = cursor.fetchone()
    return pwd, token


def get_users():
    connection, cursor = set_connection()
    cursor.execute("""SELECT * FROM Users """)
    result = cursor.fetchall()
    return result


import secrets
import string

def generate_passkey(length=12):
    """Generates a random passkey of the given length."""
    if not isinstance(length, int):
        raise TypeError("Length must be an integer.")
    if length < 8:
        raise ValueError("Length must be at least 8.")
    alphabet = string.ascii_letters + string.digits + string.punctuation
    while True:
        passkey = ''.join(secrets.choice(alphabet) for i in range(length))
        if (any(c.islower() for c in passkey)
                and any(c.isupper() for c in passkey)
                and any(c.isdigit() for c in passkey)
                and any(c in string.punctuation for c in passkey)):
            return passkey

print(secure.generate_token("testuser"))