from uuid import uuid4
from modules.users import User, UserRegistrationRequest
from typing import Optional
from percistance.connections import read_query, insert_query
from percistance.queries import ALL_USERS, USER_BY_ID, USER_BY_EMAIL, USER_BY_USERNAME, NEW_USER


session_store = {}

def get_all_users():
    data = read_query(ALL_USERS)
    return (User.from_query_result(*row) for row in data)


def get_user_by_id(user_id: int):
    data = read_query(USER_BY_ID, (user_id,))
    if not data:
        raise ValueError(f'User with ID {id} does not exist.')
    return next((User.from_query_result(*row) for row in data), None)


def get_user_by_email(email: str) -> Optional[User]:
    data = read_query(USER_BY_EMAIL, (email,))
    if not data:
        raise ValueError(f'User with email {email} does not exist.')

    return next((User.from_query_result(*row) for row in data), None)


def get_user_by_username(username: str) -> Optional[User]:
    data = read_query(USER_BY_USERNAME, (username,))
    if not data:
        raise ValueError(f'User with username {username} does not exist.')
    return next((User.from_query_result(*row) for row in data), None)


def create_user(user_data: UserRegistrationRequest):
    new_user_id = insert_query(NEW_USER, (
        user_data.username,
        user_data.email,
        user_data.password,
        1
    ))

    return new_user_id


def register_user(username: str, email: str, password: str) -> User:
    if get_user_by_username(username):
        raise ValueError('Username is already taken!')
    if get_user_by_email(email):
        raise ValueError('Email is already registered!')

    user_data = UserRegistrationRequest(username=username, email=email, password=password)
    new_user_id = create_user(user_data)
    return User(
        id=new_user_id,
        username=username,
        email=email,
        role='user',
        is_active=True
    )


def authenticate_user(email: str, password: str):
    user = get_user_by_email(email)
    if not user:
        raise ValueError(f'User with email {email} does not exist.')

    if user.password != password:
        raise ValueError('The provided password is incorrect! Please try again.')

    token = str(uuid4())

    session_store[token] = user
    return {"token": token, "token_type": "bearer"}


def create_session_token(user: User):
    token = str(uuid4())
    session_store[token] = user
    return token

def authorise_user(token: str):
    user = session_store.get(token)
    if not user:
        raise ValueError("Invalid session or expired token")
    return user