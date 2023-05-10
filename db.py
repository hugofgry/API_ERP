import psycopg2 as psy
from datetime import datetime
import secure

###
def set_connection():
    connection = psy.connect('postgres://testneon33:dfkFh5jcr1Tw@ep-hidden-forest-997741.eu-central-1.aws.neon.tech/neondb?sslmode=require')
    connection.set_session(autocommit=True)
    return connection

# Context manager for handling the connection and cursor
class DatabaseConnection:
    def __enter__(self):
        self.conn = set_connection()
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cursor.close()
        self.conn.close()

# CREATE----------------------------------------------------------------
def insert_user(username, pwd, role):
    with DatabaseConnection() as cursor:
        pwd = secure.hash_pwd(pwd)
        user = (username, pwd, role, datetime.now())
        cursor.execute(
        """
        INSERT INTO Users (username, pwd, user_role, create_at)
        VALUES (%s, %s, %s, %s)
        """,
        user
        )

# READ----------------------------------------------------------------
def get_user_pwd(username):
    with DatabaseConnection() as cursor:
        cursor.execute("""SELECT pwd FROM Users WHERE username = %s""", (str(username),))
        pwd = cursor.fetchone()
    return pwd

def get_users():
    with DatabaseConnection() as cursor:
        cursor.execute("""SELECT * FROM Users """)
        result = cursor.fetchall()
    return result

def get_user_by_token(token):
    with DatabaseConnection() as cursor:
        cursor.execute("""SELECT * FROM Users WHERE user_token = %s""", (token,))
        user = cursor.fetchone()
    return user

# UPDATE----------------------------------------------------------------
def add_user_token(username, token):
    with DatabaseConnection() as cursor:
        cursor.execute("""UPDATE Users SET user_token = %s WHERE username = %s """, (str(token), str(username)))

# DELETE----------------------------------------------------------------
def delete_user(username):
    with DatabaseConnection() as cursor:
        cursor.execute(
            """
            DELETE FROM Users 
            WHERE username = %s""",
            (str(username),)
        )
