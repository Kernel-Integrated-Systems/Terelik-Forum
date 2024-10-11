-- MAPS user_role int with user_role name
CREATE TABLE Roles (
    user_role INT PRIMARY KEY,   -- Primary key for user_role
    role_name VARCHAR(45) NOT NULL  -- Name of the role
);

-- MAPS access_level int with access_level name
CREATE TABLE UserAccessLevel (
    user_access_id INT PRIMARY KEY,   -- Primary key for access_level
    access_level VARCHAR(45) NOT NULL  -- Name of the access level: read / write / edit etc.
);

-- STORES Users data
CREATE TABLE Users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    user_role INT,  -- references the user_role in Roles table
    is_active TINYINT(1) DEFAULT 1,
    created_at DATE DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_role) REFERENCES Roles(user_role)
);

-- STORES Categories
CREATE TABLE Categories (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    category_name VARCHAR(100) UNIQUE NOT NULL,
    is_private TINYINT(1) DEFAULT 0,
    is_locked TINYINT(1) DEFAULT 0,
    created_at DATE DEFAULT CURRENT_TIMESTAMP
);

-- MAPS relationship between Users and Categories
CREATE TABLE CategoryAccess (
    user_id INT,
    category_id INT,
    access_level INT,
    PRIMARY KEY (user_id, category_id),
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (category_id) REFERENCES Categories(category_id),
    FOREIGN KEY (access_level) REFERENCES UserAccessLevel(user_access_id)
);

-- STORES Topics details
CREATE TABLE Topics (
    topic_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    user_id INT,
    category_id INT,
    is_locked TINYINT(1) DEFAULT 0,
    created_at DATE DEFAULT CURRENT_TIMESTAMP,
    best_reply_id INT,
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (category_id) REFERENCES Categories(category_id)
);

-- STORES Replies on Topics
CREATE TABLE Replies (
    reply_id INT AUTO_INCREMENT PRIMARY KEY,
    content TEXT NOT NULL,
    user_id INT,
    topic_id INT,
    created_at DATE DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (topic_id) REFERENCES Topics(topic_id)
);

-- STORES Message details
CREATE TABLE Messages (
    message_id INT AUTO_INCREMENT PRIMARY KEY,
    sender_id INT,
    recipient_id INT,
    content TEXT NOT NULL,
    created_at DATE DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sender_id) REFERENCES Users(user_id),
    FOREIGN KEY (recipient_id) REFERENCES Users(user_id)
);

-- MAPS Vote Types
CREATE TABLE VoteTypes (
    vote_id INT PRIMARY KEY,
    vote_name VARCHAR(45) NOT NULL
);

-- STORES Votes details
CREATE TABLE Votes (
    vote_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    reply_id INT,
    vote_type INT,  -- References vote_id in VoteTypes
    UNIQUE (user_id, reply_id),  -- Prevent multiple votes by same user on the same reply
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (reply_id) REFERENCES Replies(reply_id),
    FOREIGN KEY (vote_type) REFERENCES VoteTypes(vote_id)
);