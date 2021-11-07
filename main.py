from fastapi import Depends, FastAPI, HTTPException, status, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
import sqlite3

from deps import get_current_user
from forms import OAuth2PasswordRequestForm
from models import User, UserInDB

app = FastAPI()

templates = Jinja2Templates(directory="templates")


def fake_hash_password(password: str):
    return "fakehashed_" + password


@app.get("/")
def root(request: Request, current_user: User = Depends(get_current_user)):
    return templates.TemplateResponse("index.html", {"request": request, "user": current_user})


@app.get("/accounts/sign_in")
def sign_in(request: Request):
    return templates.TemplateResponse("sign_in.html", {"request": request})


@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
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
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    response.set_cookie(key="AccessToken", value=user.access_token)
    return response


@app.get("/tasks")
def task_list(request: Request, current_user: User = Depends(get_current_user)):
    sqlite_conn = sqlite3.connect('sqlite_ates.db')
    cursor = sqlite_conn.cursor()

    query = f"""SELECT description, status FROM tasks WHERE user_id = {current_user.id}"""
    cursor.execute(query)
    tasks = [{
        "description": record[0],
        "status": record[1],
    } for record in cursor.fetchall()]

    return templates.TemplateResponse("tasks.html", {
        "request": request,
        "user": current_user,
        "tasks": tasks,
    })
