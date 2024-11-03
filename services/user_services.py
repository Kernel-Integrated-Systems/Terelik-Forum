import jwt
from fastapi import HTTPException
from modules.users import User, UserRegistrationRequest, TokenResponse, UserAccess
from typing import Optional
from percistance.connections import read_query, insert_query
from percistance import queries
import datetime

from web_routers.router_users import users_router


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


def validate_new_user_credentials(user: str, email: str) -> bool:
    user_exists = read_query(queries.USER_EXISTS, (user, email))
    if len(user_exists) == 0:
        return False
    return True

def create_user(user_data: UserRegistrationRequest):
    new_user_id = insert_query(queries.NEW_USER, (
        user_data.username,
        user_data.email,
        user_data.password,
        1
    ))

    return new_user_id


def register_user(username: str, email: str, password: str) -> User:
    user_exists = validate_new_user_credentials(username, email)
    if user_exists:
        raise ValueError('An user with the same username or password already exists!')

    user_data = UserRegistrationRequest(username=username, email=email, password=password)
    new_user_id = create_user(user_data)
    return User(
        id=new_user_id,
        username=username,
        email=email,
        role=1,
        is_active=True
    )


def authenticate_user(username: str, password: str) -> str:
    user = read_query(queries.LOGIN_USERNAME_PASS, (username, password))
    if not user:
        raise ValueError(f'User with username {username} does not exist.')

    if user[0][2] != password:
        raise ValueError('The provided password is incorrect! Please try again.')

    token = create_jwt_token(user[0][0], user[0][1], user[0][3])
    return token


def logout_user(username: str, token: str):
    token_data = decode_jwt_token(token)
    if token_data["user"] != username:
        raise ValueError(f'User {username} is not logged in.')

    session_token = read_query(queries.SEARCH_TOKEN, (token,))
    print(session_token)
    return {"message": f"User {username} successfully logged out."}

""" 
----------------------------------->
    Аuthentication 
        Logic 
    and token JWT 
----------------------------------->
"""


SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"


def create_jwt_token(user_id: int, username: str, user_role: int) -> str:
    expiration = datetime.datetime.now() + datetime.timedelta(days=1)  # Token valid for 1 day


    token_data = {
        "sub": username,
        "user_id": user_id,
        "user_role": user_role,
        "exp": expiration
    }
    token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
    return token


def decode_jwt_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return {
            "user_id": payload["user_id"],
            "username": payload["sub"],
            "user_role": payload["user_role"]
        }

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired.")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token.")


def authenticate(authorization: str) -> dict:
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization token missing or invalid")

    # token = authorization.split(" ")[1]
    decoded_token = decode_jwt_token(authorization)

    return decoded_token


def get_token_user(authorization: str) -> User | None:
    if authorization:
        user_obj = authenticate(authorization)
        user = get_user_by_id(user_obj["user_id"])
        return user
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