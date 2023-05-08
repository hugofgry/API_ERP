import psycopg2 as psy
import db

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


print(get_users())
