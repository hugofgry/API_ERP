import psycopg2 as psy
from datetime import datetime, timedelta
import secure

def set_connection():
  connection = psy.connect('postgres://testneon33:dfkFh5jcr1Tw@ep-hidden-forest-997741.eu-central-1.aws.neon.tech/neondb?sslmode=require')
  connection.set_session(autocommit=True)
  cursor = connection.cursor()
  return connection, cursor


def insert(username, pwd, role, token) :

  connection, cursor = set_connection()
  pwd = secure.hash_pwd(pwd)
  user = (username, pwd, role, token, datetime.datetime.now())
  cursor.execute(
  """
  INSERT INTO Users (username, pwd, role, token, create_at)
  VALUES (%s, %s, %s, %s, %s),user
  """,
  user
  )
  connection.close()


# CREATE----------------------------------------------------------------

def insert_user(username, pwd, role):
  connection, cursor = set_connection()
  pwd = secure.hash_pwd(pwd)
  user = (username, pwd, role, datetime.now())
  cursor.execute(
  """
  INSERT INTO Users (username, pwd, user_role, create_at)
  VALUES (%s, %s, %s, %s)
  """,
  user
  )
  connection.close()


# READ----------------------------------------------------------------

def get_user_pwd(username):

    connection,cursor = set_connection()
    cursor.execute("""SELECT pwd FROM Users WHERE username = %s""", (str(username),))
    pwd = cursor.fetchone()
    connection.close()

    return pwd


def get_users():
    connection, cursor = set_connection()
    cursor.execute("""SELECT * FROM Users """)
    result = cursor.fetchall()
    connection.close()

    return result

# UPDATE----------------------------------------------------------------


def add_user_token(username, token):
  connection, cursor = set_connection()
  cursor.execute("""UPDATE Users SET user_token = %s WHERE username = %s """,(str(token),str(username)))
  connection.close()


# DELETE----------------------------------------------------------------

def delete_user(username):
  connection, cursor = set_connection()
  cursor.execute(
    """
    DELETE FROM Users 
    WHERE username = %s""",
    (str(username),)
  )
  connection.close()





