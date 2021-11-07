import uuid
import sqlite3

from forms import OAuth2PasswordRequestForm
from models import UserInDB


class IncorrectCredentials(Exception):
    pass


def fake_hash_password(password: str):
    return "fakehashed_" + password


def is_user_exists(email: str) -> bool:
    sqlite_conn = sqlite3.connect('sqlite_ates.db')
    cursor = sqlite_conn.cursor()

    query = f"""SELECT id FROM users where email='{email}'"""
    cursor.execute(query)
    records = cursor.fetchall()
    if records:
        return True
    return False


def create_user(form_data: OAuth2PasswordRequestForm) -> str:
    sqlite_conn = sqlite3.connect('sqlite_ates.db')
    cursor = sqlite_conn.cursor()

    hashed_password = fake_hash_password(form_data.password)
    access_token = str(uuid.uuid4())

    sqlite_insert_query = (f"""INSERT INTO users
            (email, hashed_password, role, access_token, full_name)
            VALUES ('{form_data.email}', '{hashed_password}', 'manager', '{access_token}', 'Попуг Иванович')""")
    cursor.execute(sqlite_insert_query)
    sqlite_conn.commit()

    return access_token


def get_user(form_data: OAuth2PasswordRequestForm) -> UserInDB:
    sqlite_conn = sqlite3.connect('sqlite_ates.db')
    cursor = sqlite_conn.cursor()

    query = (f"""SELECT id, email, hashed_password, access_token, full_name
        FROM users
        WHERE email = '{form_data.email}'""")
    cursor.execute(query)
    records = cursor.fetchall()
    if records:
        record = records[0]
        user = UserInDB(
            id=record[0],
            email=record[1],
            full_name=record[4],
            hashed_password=record[2],
            access_token=record[3],
        )
    else:
        raise IncorrectCredentials

    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise IncorrectCredentials

    return user
