import sqlite3


def ensure_connection(func):
    def decorator(*args, **kwargs):
        with sqlite3.connect('database.db') as conn:
            result = func(conn, *args, **kwargs)
        return result
    return decorator


@ensure_connection
def init_db(conn, force: bool = False):
    c = conn.cursor()
    if force:
        c.execute("DROP TABLE IF EXISTS users")
    c.execute("""CREATE TABLE IF NOT EXISTS users (
        id              INTEGER PRIMARY KEY,
        first_name                   STRING,
        last_name                    STRING,
        date                         STRING,
        user_id                     INTEGER,
        button                       STRING,
        calendar_date                STRING,
        title                        STRING,
        link                         STRING);
    """)
    conn.commit()


@ensure_connection
def user_info(conn, first_name: str, last_name: str, date: str, user_id, button: str, calendar_date: str, title: str, link: str):
    c = conn.cursor()
    c.execute("INSERT INTO users (first_name, last_name, date, user_id, button, calendar_date, title, link) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
              (first_name, last_name, date, user_id, button, calendar_date, title, link))
    conn.commit()


@ensure_connection
def return_history(conn, user_id):
    c = conn.cursor()
    c.execute("SELECT button, calendar_date, title, link FROM users WHERE user_id = ?", (user_id,))
    history = c.fetchall()
    history = history[::-1]
    return history

