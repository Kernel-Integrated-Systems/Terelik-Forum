# from mariadb import connect
# from mariadb.connections import Connection
from data.database import _DB_FILE
from sqlite3 import connect

# MariaDB connectors
# def _get_connection() -> Connection:
#     return connect(
#         user='root',
#         password='L005et@62#Py7Hon',
#         host='localhost',
#         port=3306,
#         database='ordering_api_db_v2'
#     )
#
#
# def read_query(sql: str, sql_params=()):
#     with _get_connection() as conn:
#         cursor = conn.cursor()
#         cursor.execute(sql, sql_params)
#
#         return list(cursor)
#
# def insert_query(sql: str, sql_params=()) -> int:
#     with _get_connection() as conn:
#         cursor = conn.cursor()
#         cursor.execute(sql, sql_params)
#         conn.commit()
#
#         return cursor.lastrowid
#
# def update_query(sql: str, sql_params=()) -> bool:
#     with _get_connection() as conn:
#         cursor = conn.cursor()
#         cursor.execute(sql, sql_params)
#         conn.commit()
#
#         return cursor.rowcount

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
