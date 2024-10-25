from sqlite3 import connect


# Global variable to store the database file path
_DB_FILE = './data/forum_api.db'  # Adjust the path as needed


def query_count(sql: str, sql_params=()):
    with connect(_DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute(sql, sql_params)

        return cursor.fetchone()[0]


