# USER QUERIES

ALL_USERS = """SELECT user_id, username, email, user_role, is_active FROM users"""
USER_BY_ID = """SELECT user_id, username, email, user_role, is_active FROM users WHERE user_id = ?"""
USER_BY_EMAIL = """SELECT user_id, username, email, user_role, is_active FROM users WHERE email = ?"""
USER_BY_USERNAME = """SELECT user_id, username, email, user_role, is_active FROM users WHERE username = ?"""
NEW_USER = """INSERT INTO Users (username, email, password_hash, user_role)
            VALUES (?, ?, ?, ?)"""
LOGIN_USERNAME_PASS = """SELECT user_id, username, password_hash, user_role FROM users
            WHERE username = ? AND password_hash = ?"""

INSERT_TOKEN = """INSERT INTO sessions (token_string, expiration_time)
            VALUES (?, ?)"""
SEARCH_TOKEN = """SELECT * FROM sessions WHERE Token_String = ?"""

# USER ACCESS QUERIES

REMOVE_ACCESS = "DELETE FROM CategoryAccess WHERE user_id = ? AND category_id = ? "
GET_ACCESS_LEVEL = """
        SELECT ca.access_level 
        FROM CategoryAccess ca
        JOIN Categories c ON ca.category_id = c.category_id
        WHERE ca.user_id = ? AND ca.category_id = ? AND c.is_private = 1
    """
GRANT_READ_ACCESS = """INSERT INTO CategoryAccess (user_id, category_id, access_level) 
               VALUES (?, ?, 1) 
               ON CONFLICT(user_id, category_id) DO UPDATE SET access_level = 1"""
GRANT_WRITE_ACCESS = """
        INSERT INTO CategoryAccess (user_id, category_id, access_level) 
        VALUES (?, ?, 2) 
        ON CONFLICT(user_id, category_id) 
        DO UPDATE SET access_level = 2
    """
USER_CATEGORIES = """
        SELECT c.category_id, c.category_name, c.is_private, c.is_locked
        FROM categories c
        JOIN CategoryAccess ca ON c.category_id = ca.category_id
        WHERE ca.user_id = ? AND c.is_locked = 1
    """

GET_USER_ACCESSIBLE_CATEGORIES= """
       SELECT c.category_id, c.category_name, c.is_private, c.is_locked
       FROM categories c
       JOIN CategoryAccess ca ON c.category_id = ca.category_id
       WHERE ca.user_id = ? AND c.is_locked = 1
   """

# TOPICS QUERIES

ALL_TOPICS = """SELECT topic_id, title, content, user_id, category_id FROM topics"""
TOPIC_BY_ID = """SELECT topic_id, title, content, user_id, category_id, is_locked FROM topics
            WHERE topic_id = ?"""
TOPIC_BY_TITLE = """SELECT topic_id, title, content, user_id, category_id FROM topics
            WHERE title = ?"""
TOPIC_BY_CATEGORY = """SELECT topic_id, title, content, user_id, category_id FROM topics
            WHERE category_id = ?"""
NEW_TOPIC = """INSERT INTO topics (title, content, user_id, category_id)
            VALUES (?, ?, ?, ?)"""
DELETE_TOPIC = """DELETE FROM topics WHERE topic_id = ?"""
CHANGE_TOPIC_LOCK_STATUS = """UPDATE Topics SET is_locked = ? WHERE category_id = ?"""
CHECK_TOPIC_PRIVATE_STATUS = """SELECT is_locked FROM Topics WHERE topic_id = ?"""

# MESSAGE QUERIES

ALL_MESSAGES = """SELECT 
                se.username AS sender, 
                re.username AS receiver, 
                GROUP_CONCAT(m.content, ', ') AS messages
            FROM messages m
            LEFT JOIN users se ON se.user_id = m.sender_id
            LEFT JOIN users re ON re.user_id = m.recipient_id
            WHERE se.user_id = ? OR re.user_id = ?
            GROUP BY se.username, re.username"""

MESSAGE_BY_ID = """SELECT 
                se.username AS sender, re.username AS receiver, 
                GROUP_CONCAT(m.content, ', ') AS messages
            FROM messages m
            LEFT JOIN users se ON se.user_id = m.sender_id
            LEFT JOIN users re ON re.user_id = m.recipient_id
            WHERE se.user_id = ? AND re.user_id = ?
            GROUP BY se.username, re.username"""

NEW_MESSAGE = """INSERT INTO messages (sender_id, recipient_id, content) VALUES (?, ?, ?)"""


# CATEGORIES QUERIES

ALL_CATEGORIES = """SELECT category_id, category_name, is_private, is_locked FROM categories"""

CATEGORY_BY_ID = """SELECT category_id, category_name, is_private, is_locked FROM categories
            WHERE category_id = ?"""

CATEGORY_BY_NAME = """SELECT category_id, category_name, is_private, is_locked FROM categories WHERE category_name = ?"""

NEW_CATEGORY = """INSERT INTO categories (category_name) VALUES (?)"""

DELETE_CATEGORY = """DELETE FROM categories WHERE category_id = ?"""

CATEGORY_PRIVILEGED_USERS = """SELECT a.category_id, c.category_name, u.username, ac.access_level FROM categoryaccess a
            LEFT JOIN categories c on a.category_id = c.category_id
            LEFT JOIN users u on a.user_id = u.user_id
            LEFT JOIN useraccesslevel ac on a.access_level = ac.user_access_id
            WHERE a.category_id = ?"""

# REPLIES QUERIES

REPLIES_FOR_TOPIC = """SELECT * FROM replies WHERE topic_id = ?"""
VOTE_ON_REPLY = """INSERT INTO votes (user_id, reply_id, vote_type) VALUES (?, ?, ?)"""

NEW_REPLY = """INSERT INTO replies (content, user_id, topic_id) VALUES (?, ?, ?)"""

CHOOSE_BEST_REPLY_ID = """SELECT reply_id FROM replies
            WHERE user_id = ? AND topic_id = ? AND reply_id = ?"""

ADD_BEST_REPLY_ON_TOPIC = """UPDATE topics SET best_reply_id = ?
            WHERE topic_id = ?"""
