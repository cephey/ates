import sqlite3


def get_tasks_by_user_id(user_id):
    sqlite_conn = sqlite3.connect('sqlite_ates.db')
    cursor = sqlite_conn.cursor()

    query = f"""SELECT description, status FROM tasks WHERE user_id = {user_id}"""
    cursor.execute(query)
    return [{
        "description": record[0],
        "status": record[1],
    } for record in cursor.fetchall()]
