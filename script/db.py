import psycopg2 as psy
from datetime import datetime, timedelta

def set_connection():
  connection = psy.connect('postgres://testneon33:dfkFh5jcr1Tw@ep-hidden-forest-997741.eu-central-1.aws.neon.tech/neondb')
  connection.set_session(autocommit=True)
  cursor = connection.cursor()
  return connection, cursor


def insert(username, pwd, role, token) :

  connection, cursor = set_connection()
  user = (username, pwd, role, token, datetime.datetime.now())
  cursor.execute(
  """
  INSERT INTO Users (username, pwd, role, token, create_at)
  VALUES (%s, %s, %s, %s, %s),user
  """,
  user
  )
  connection.close()


def get_user_pwd_and_token(user_name):

    connection,cursor = set_connection()
    cursor.execute("""SELECT pwd,user_token FROM Users WHERE username = %s""", (str(user_name),))
    pwd, token = cursor.fetchone()
    return pwd, token


def insert_admin_user(username, pwd, role):
  connection, cursor = set_connection()
  token = generate_token("username")
  user = (username, pwd, role, token, datetime.now())
  cursor.execute(
  """
  INSERT INTO Users (username, pwd, user_role, user_token, create_at)
  VALUES (%s, %s, %s, %s, %s)
  """,
  user
  )
  connection.close()




