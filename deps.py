from fastapi import Depends, HTTPException, status
import sqlite3

from models import UserInDB
from oauth2 import OAuth2Cookie

oauth2_scheme = OAuth2Cookie(tokenUrl="token", auto_error=False)


def get_user(token: str):
    sqlite_conn = sqlite3.connect('sqlite_ates.db')
    cursor = sqlite_conn.cursor()

    query = (f"""SELECT id, email, hashed_password, access_token, full_name
    FROM users
    WHERE access_token = '{token}'
    """)
    cursor.execute(query)

    records = cursor.fetchall()
    if records:
        record = records[0]
        return UserInDB(
            id=record[0],
            email=record[1],
            full_name=record[4],
            hashed_password=record[2],
            access_token=record[4],
        )


def get_current_user(token: str = Depends(oauth2_scheme)):
    user = get_user(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_302_FOUND,
            detail="Invalid authentication credentials",
            headers={"Location": "/accounts/sign_in"},
        )
    return user
