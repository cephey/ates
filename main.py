import json

from fastapi import Depends, FastAPI, HTTPException, status, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from deps import get_current_user
from forms import OAuth2PasswordRequestForm
from kafka import KafkaConsumer, KafkaProducer
from models import User
from task_repo import get_tasks_by_user_id
from user_repo import create_user, is_user_exists, get_user, IncorrectCredentials

app = FastAPI()

templates = Jinja2Templates(directory="templates")


@app.get("/")
def root(request: Request, current_user: User = Depends(get_current_user)):
    return templates.TemplateResponse("index.html", {"request": request, "user": current_user})


@app.get("/accounts/sign_up")
def sign_up(request: Request):
    return templates.TemplateResponse("sign_up.html", {"request": request})


@app.post("/registration")
def registration(form_data: OAuth2PasswordRequestForm = Depends()):
    if is_user_exists(form_data.email):
        raise HTTPException(status_code=400, detail="Username already exists")

    user = create_user(form_data)

    producer = KafkaProducer(
        bootstrap_servers='localhost:9092',
        value_serializer=lambda v: json.dumps(v).encode('utf-8'),
        max_block_ms=5_000,
    )
    producer.send('test', value={'id': user.id, 'token': user.access_token})

    response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    response.set_cookie(key="AccessToken", value=user.access_token)
    return response


@app.get("/accounts/sign_in")
def sign_in(request: Request):
    return templates.TemplateResponse("sign_in.html", {"request": request})


@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        user = get_user(form_data)
    except IncorrectCredentials as exc:
        raise HTTPException(status_code=400, detail="Incorrect username or password") from exc

    response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    response.set_cookie(key="AccessToken", value=user.access_token)
    return response


@app.get("/tasks")
def task_list(request: Request, current_user: User = Depends(get_current_user)):
    tasks = get_tasks_by_user_id(current_user.id)
    return templates.TemplateResponse("tasks.html", {
        "request": request,
        "user": current_user,
        "tasks": tasks,
    })
