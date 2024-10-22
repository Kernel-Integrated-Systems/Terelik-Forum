from modules.users import User, UserRegistrationRequest
from typing import Optional
from percistance.connections import read_query, insert_query
from percistance.data import session_store, create_jwt_token, decode_jwt_token
from percistance.queries import ALL_USERS, USER_BY_ID, USER_BY_EMAIL, USER_BY_USERNAME, NEW_USER, LOGIN_USERNAME_PASS


def get_all_users():
    data = read_query(ALL_USERS)
    return (User.from_query_result(*row) for row in data)


def get_user_by_id(user_id: int):
    data = read_query(USER_BY_ID, (user_id,))
    if not data:
        raise ValueError(f'User with ID {user_id} does not exist.')
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
    usernm = read_query(USER_BY_USERNAME, (username,))
    userem = read_query(USER_BY_EMAIL, (email,))
    if usernm:
        raise ValueError(f'Username {username} is already taken!')
    if userem:
        raise ValueError(f'Email {email} is already registered!')

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
    user = read_query(LOGIN_USERNAME_PASS, (username, password))
    if not user:
        raise ValueError(f'User with username {username} does not exist.')

    if user[0][2] != password:
        raise ValueError('The provided password is incorrect! Please try again.')


    user_id = user[0][0]
    user_role = user[0][3]
    token = create_jwt_token(user_id, username, user_role)

    session_store[token] = {
        "username": username,
        "user_id": user_id,
        "user_role": user_role
    }

    return {"token": token, "token_type": "bearer"}


def un_authenticate_user(username: str):
    for token, user_info in list(session_store.items()):
        if user_info.get("username") == username:
            del session_store[token]
            return {"message": f"User {username} successfully logged out."}

    raise ValueError(f'User {username} is not logged in or session has expired.')
