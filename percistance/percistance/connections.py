# from mariadb import connect
# from mariadb.connections import Connection
from data.database import _DB_FILE
from sqlite3 import connect


# SQLite connectors
def read_query(sql: str, sql_params=()):
    with connect(_DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute(sql, sql_params)

        return list(cursor)


def insert_query(sql: str, sql_params=()) -> int:
    with connect(_DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute(sql, sql_params)
        conn.commit()

        return cursor.lastrowid


def update_query(sql: str, sql_params=()) -> bool:
    with connect(_DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute(sql, sql_params)
        conn.commit()

        return cursor.rowcount > 0
