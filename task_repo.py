import sqlite3
import uuid

from forms import TaskAddForm
from models import User, TaskInDB


def get_tasks_by_user_id(user_id):
    sqlite_conn = sqlite3.connect('sqlite_ates.db')
    cursor = sqlite_conn.cursor()

    query = f"""SELECT public_id, title, description, status FROM tasks WHERE user_id = {user_id}"""
    cursor.execute(query)
    return [{
        "public_id": record[0],
        "title": record[1],
        "description": record[2],
        "status": record[3],
    } for record in cursor.fetchall()]


def create_task(form_data: TaskAddForm, user: User) -> TaskInDB:
    sqlite_conn = sqlite3.connect('sqlite_ates.db')
    cursor = sqlite_conn.cursor()

    public_uuid = str(uuid.uuid4())
    status = 'new'

    sqlite_insert_query = (f"""INSERT INTO tasks
            (public_id, user_id, title, description, status)
            VALUES ('{public_uuid}', {user.id}, '{form_data.title}', '{form_data.description}', '{status}')""")
    cursor.execute(sqlite_insert_query)
    sqlite_conn.commit()

    query = f"""SELECT id, user_id, title, description, status FROM tasks WHERE public_id = '{public_uuid}' ORDER BY id DESC"""
    cursor.execute(query)
    records = cursor.fetchall()
    record = records[0]
    task = TaskInDB(
        id=record[0],
        user_id=record[1],
        title=record[2],
        description=record[3],
        status=record[4],
        public_id=public_uuid,
    )
    return task
