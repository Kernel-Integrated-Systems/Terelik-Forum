import mariadb



def read_query(database: str, database_params=()):
    with _conn_to_db() as conn:
        cursor = conn.cursor()
        cursor.execute(database, database_params)

        return list(cursor)


def insert_query(database: str, database_params=()) -> int:
    with _conn_to_db() as conn:
        cursor = conn.cursor()
        cursor.execute(database, database_params)
        conn.commit()

        return cursor.lastrowid
#

def update_query(database: str, database_params=()):
    with _conn_to_db() as conn:
        cursor = conn.cursor()
        cursor.execute(database, database_params)
        conn.commit()

        return cursor.rowcount > 0






def _conn_to_db():
    return mariadb.connect(
        host="127.0.0.1",
        port=3306,
        user="root",
        password="pass",
        database='forum_api_db')