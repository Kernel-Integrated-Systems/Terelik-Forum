# USER QUERIES

ALL_USERS = """SELECT user_id, username, email, user_role, is_active FROM users"""
USER_BY_ID = """SELECT user_id, username, email, user_role, is_active FROM users WHERE user_id = ?"""
USER_BY_EMAIL = """SELECT user_id, username, email, user_role, is_active FROM users WHERE email = ?"""
USER_BY_USERNAME = """SELECT user_id, username, email, user_role, is_active FROM users WHERE username = ?"""
NEW_USER = """INSERT INTO Users (username, email, password_hash, user_role)
            VALUES (?, ?, ?, ?)"""