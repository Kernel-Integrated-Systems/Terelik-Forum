from fastapi import HTTPException
from modules.users import User, UserRegistrationRequest, TokenResponse, UserAccess
from typing import Optional
import base64
from percistance.connections import read_query, insert_query
from percistance import queries
from datetime import datetime


def get_all_users():
    data = read_query(queries.ALL_USERS)
    return (User.from_query_result(*row) for row in data)


def get_user_by_id(user_id: int):
    data = read_query(queries.USER_BY_ID, (user_id,))
    if not data:
        raise ValueError(f'User with ID {id} does not exist.')
    return next((User.from_query_result(*row) for row in data), None)


def get_user_by_email(email: str) -> Optional[User]:
    data = read_query(queries.USER_BY_EMAIL, (email,))
    if not data:
        raise ValueError(f'User with email {email} does not exist.')

    return next((User.from_query_result(*row) for row in data), None)


def get_user_by_username(username: str) -> Optional[User]:
    data = read_query(queries.USER_BY_USERNAME, (username,))
    if not data:
        raise ValueError(f'User with username {username} does not exist.')
    return next((User.from_query_result(*row) for row in data), None)


def create_user(user_data: UserRegistrationRequest):
    new_user_id = insert_query(queries.NEW_USER, (
        user_data.username,
        user_data.email,
        user_data.password,
        1
    ))

    return new_user_id


def register_user(username: str, email: str, password: str) -> User:
    usernm = get_user_by_username(username)
    userem = get_user_by_email(email)
    if usernm:
        raise ValueError(f'Username {username} is already taken!')
    if userem:
        raise ValueError(f'Email is {email} already registered!')

    user_data = UserRegistrationRequest(username=username, email=email, password=password)
    new_user_id = create_user(user_data)
    return User(
        id=new_user_id,
        username=username,
        email=email,
        role=1,
        is_active=True
    )


def authenticate_user(username: str, password: str):
    user = read_query(queries.LOGIN_USERNAME_PASS, (username, password))
    if not user:
        raise ValueError(f'User with email {username} does not exist.')

    if user[0][2] != password:
        raise ValueError('The provided password is incorrect! Please try again.')
    # assign user_id, username and user_role
    token = encode(user[0][0], user[0][1], user[0][3])
    return TokenResponse(access_token=token)


def logout_user(username: str, token: str):
    token_data = decode(token)
    if token_data["user"] != username:
        raise ValueError(f'User {username} is not logged in.')

    session_token = read_query(queries.SEARCH_TOKEN, (token,))
    print(session_token)
    return {"message": f"User {username} successfully logged out."}


def authenticate(token) -> dict:
    session_data = decode(token)
    user = get_user_by_username(session_data["username"])
    if not user:
        raise ValueError(f'Username {session_data["username"]} is not registered or token has expired.')

    return session_data


def encode(user_id: int, username: str, user_role: int) -> str:
    now = datetime.now()
    user_string = f"{user_id}_{username}_{user_role}_{now.strftime("%H:%M:%S")}"
    encoded_bytes = base64.b64encode(user_string.encode('utf-8'))

    return encoded_bytes.decode('utf-8')


def decode(encoded_value: str):
    decoded_string = base64.b64decode(encoded_value).decode('utf-8')
    user_id, username, user_role, created_at = decoded_string.split('_')
    result = {
        "user_id": int(user_id),
        "username": username,
        "user_role": int(user_role),
        "created_at": created_at
    }
    return result


"""
----------------------------------->
Permissions for users ACCESS LEVELS
----------------------------------->
"""

def get_access_level(user_id: int, category_id: int):
    data = read_query(queries.GET_ACCESS_LEVEL, (user_id, category_id))
    if not data:
        return None
    return data[0][0]


def grant_read_access(user_id: int, category_id: int) -> dict:
    user_access = UserAccess(user_id=user_id, category_id=category_id, access_level=1)
    insert_query(queries.GRANT_READ_ACCESS, (user_access.user_id, user_access.category_id))
    return {"message": f"User {user_access.user_id} granted read access to category {user_access.category_id}"}


def grant_write_access(user_id: int, category_id: int) -> dict:
    user_access = UserAccess(user_id=user_id, category_id=category_id, access_level=2)
    insert_query(queries.GRANT_WRITE_ACCESS, (user_access.user_id, user_access.category_id))
    return {"message": f"User {user_access.user_id} granted write access to category {user_access.category_id}"}


def revoke_access(user_id: int, category_id: int):
    user_access = get_access_level(user_id, category_id)

    if user_access:
        insert_query(queries.REMOVE_ACCESS, (user_id, category_id))
        return {"message": f"User {user_id}'s access to category {category_id} has been revoked."}
    else:
        raise ValueError(f"Failed to revoke access for user {user_id} to category {category_id}.")