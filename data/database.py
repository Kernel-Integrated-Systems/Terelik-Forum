from sqlite3 import connect


# Global variable to store the database file path
_DB_FILE = './data/forum_api.db'  # Adjust the path as needed


def query_count(sql: str, sql_params=()):
    with connect(_DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute(sql, sql_params)

        return cursor.fetchone()[0]


def database_init():
    # Use a with statement to ensure the connection is properly managed
    with connect(_DB_FILE) as conn:
        cursor = conn.cursor()

        # Create tables
        cursor.execute("""CREATE TABLE IF NOT EXISTS Roles (
                            user_role INTEGER PRIMARY KEY, 
                            role_name TEXT NOT NULL
                          )""")

        cursor.execute("""CREATE TABLE IF NOT EXISTS UserAccessLevel (
                            user_access_id INTEGER PRIMARY KEY,   
                            access_level TEXT NOT NULL 
                          )""")

        cursor.execute("""CREATE TABLE IF NOT EXISTS Users (
                            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                            username TEXT UNIQUE NOT NULL,
                            email TEXT UNIQUE NOT NULL,
                            password_hash TEXT NOT NULL,
                            user_role INTEGER,
                            is_active INTEGER DEFAULT 1,
                            created_at DATE DEFAULT CURRENT_TIMESTAMP,
                            FOREIGN KEY (user_role) REFERENCES Roles(user_role)
                          )""")

        cursor.execute("""CREATE TABLE IF NOT EXISTS Categories (
                            category_id INTEGER PRIMARY KEY AUTOINCREMENT,
                            category_name TEXT UNIQUE NOT NULL,
                            is_private INTEGER DEFAULT 0,
                            is_locked INTEGER DEFAULT 0,
                            created_at DATE DEFAULT CURRENT_TIMESTAMP
                          )""")

        cursor.execute("""CREATE TABLE IF NOT EXISTS CategoryAccess (
                            user_id INTEGER,
                            category_id INTEGER,
                            access_level INTEGER,
                            PRIMARY KEY (user_id, category_id),
                            FOREIGN KEY (user_id) REFERENCES Users(user_id),
                            FOREIGN KEY (category_id) REFERENCES Categories(category_id),
                            FOREIGN KEY (access_level) REFERENCES UserAccessLevel(user_access_id)
                          )""")

        cursor.execute("""CREATE TABLE IF NOT EXISTS Topics (
                            topic_id INTEGER PRIMARY KEY AUTOINCREMENT,
                            title TEXT NOT NULL,
                            content TEXT NOT NULL,
                            user_id INTEGER,
                            category_id INTEGER,
                            is_locked INTEGER DEFAULT 0,
                            created_at DATE DEFAULT CURRENT_TIMESTAMP,
                            best_reply_id INTEGER,
                            FOREIGN KEY (user_id) REFERENCES Users(user_id),
                            FOREIGN KEY (category_id) REFERENCES Categories(category_id)
                          )""")

        cursor.execute("""CREATE TABLE IF NOT EXISTS Replies (
                            reply_id INTEGER PRIMARY KEY AUTOINCREMENT,
                            content TEXT NOT NULL,
                            user_id INTEGER,
                            topic_id INTEGER,
                            created_at DATE DEFAULT CURRENT_TIMESTAMP,
                            FOREIGN KEY (user_id) REFERENCES Users(user_id),
                            FOREIGN KEY (topic_id) REFERENCES Topics(topic_id)
                          )""")

        cursor.execute("""CREATE TABLE IF NOT EXISTS Messages (
                            message_id INTEGER PRIMARY KEY AUTOINCREMENT,
                            sender_id INTEGER,
                            recipient_id INTEGER,
                            content TEXT NOT NULL,
                            created_at DATE DEFAULT CURRENT_TIMESTAMP,
                            FOREIGN KEY (sender_id) REFERENCES Users(user_id),
                            FOREIGN KEY (recipient_id) REFERENCES Users(user_id)
                          )""")

        cursor.execute("""CREATE TABLE IF NOT EXISTS VoteTypes (
                            vote_id INTEGER PRIMARY KEY,
                            vote_name TEXT NOT NULL
                          )""")

        cursor.execute("""CREATE TABLE IF NOT EXISTS Votes (
                            vote_id INTEGER PRIMARY KEY AUTOINCREMENT,
                            user_id INTEGER,
                            reply_id INTEGER,
                            vote_type INTEGER,
                            UNIQUE (user_id, reply_id),
                            FOREIGN KEY (user_id) REFERENCES Users(user_id),
                            FOREIGN KEY (reply_id) REFERENCES Replies(reply_id),
                            FOREIGN KEY (vote_type) REFERENCES VoteTypes(vote_id)
                          )""")

        cursor.execute("""CREATE TABLE IF NOT EXISTS SecretKeys (secret VARCHAR(200))""")

        cursor.execute("""CREATE TABLE IF NOT EXISTS  Sessions (
                            Token_String VARCHAR(255) NOT NULL,
                            Created_at DATE,
                            Expiration_time INT,
                            Expired TINYINT(1) DEFAULT 0
                        )""")

        # Insert initial data (if needed)
        if query_count("SELECT COUNT(*) FROM roles") == 0:
            cursor.execute("INSERT OR IGNORE INTO Roles VALUES "
                       "(1, 'User'), "
                       "(2, 'Admin')")

        if query_count("SELECT COUNT(*) FROM useraccesslevel") == 0:
            cursor.execute("INSERT OR IGNORE INTO UserAccessLevel VALUES "
                       "(1, 'Read'), "
                       "(2, 'Full Control')")

        if query_count("SELECT COUNT(*) FROM users") == 0:
            cursor.execute("""INSERT INTO Users (username, email, password_hash, user_role, is_active) VALUES
                        ('alice', 'alice@example.com', 'hashed_password_1', 1, 1),
                        ('bob', 'bob@example.com', 'hashed_password_2', 2, 1),
                        ('charlie', 'charlie@example.com', 'hashed_password_3', 1, 1),
                        ('dave', 'dave@example.com', 'hashed_password_4', 1, 0),
                        ('eve', 'eve@example.com', 'hashed_password_5', 1, 1)""")

        if query_count("SELECT COUNT(*) FROM categories") == 0:
            cursor.execute("""INSERT INTO Categories (category_name, is_private, is_locked) VALUES
                        ('General Discussion', 0, 0),
                        ('Announcements', 0, 1),
                        ('Off-Topic', 0, 0),
                        ('Tech Support', 0, 0),
                        ('Private Forum', 1, 1)""")

        if query_count("SELECT COUNT(*) FROM categoryaccess") == 0:
            cursor.execute("""INSERT INTO CategoryAccess (user_id, category_id, access_level) VALUES
                        (1, 1, 1),
                        (2, 1, 2),
                        (3, 1, 1),
                        (4, 5, 1),
                        (5, 2, 1)""")

        if query_count("SELECT COUNT(*) FROM topics") == 0:
            cursor.execute("""INSERT INTO Topics (title, content, user_id, category_id) VALUES
                        ('Welcome to the Forum', 'This is the first post.', 1, 1),
                        ('Forum Rules', 'Please read the rules before posting.', 2, 2),
                        ('Off-Topic Banter', 'Let’s talk about anything here.', 3, 3),
                        ('How to fix login issues?', 'I cannot log in, help needed.', 4, 4),
                        ('Private Forum Topic', 'This is a private discussion.', 5, 5)""")

        if query_count("SELECT COUNT(*) FROM replies") == 0:
            cursor.execute("""INSERT INTO Replies (content, user_id, topic_id) VALUES
                        ('Thanks for the welcome!', 3, 1),
                        ('Understood the rules, thank you.', 4, 2),
                        ('I love off-topic banter!', 2, 3),
                        ('Try resetting your password.', 1, 4),
                        ('Can anyone see this?', 5, 5)""")

        if query_count("SELECT COUNT(*) FROM messages") == 0:
            cursor.execute("""INSERT INTO Messages (sender_id, recipient_id, content) VALUES
                        (1, 2, 'Hey, how are you?'),
                        (2, 3, 'Can you help me with something?'),
                        (3, 4, 'Nice to meet you!'),
                        (4, 1, 'I have an issue with my account.'),
                        (5, 3, 'Are you available for a chat?')""")

        if query_count("SELECT COUNT(*) FROM votetypes") == 0:
            cursor.execute("""INSERT INTO VoteTypes (vote_id, vote_name) VALUES
                        (1, 'Upvote'),
                        (2, 'Downvote')""")

        if query_count("SELECT COUNT(*) FROM votes") == 0:
            cursor.execute("""INSERT INTO Votes (user_id, reply_id, vote_type) VALUES
                        (1, 1, 1),
                        (2, 2, 1),
                        (3, 3, 1),
                        (4, 4, 2),
                        (5, 5, 2)""")

        if query_count("SELECT COUNT(*) FROM SecretKeys") == 0:
            cursor.execute("""INSERT INTO SecretKeys VALUES ('secret')""")

        print("Database initialized successfully.")
