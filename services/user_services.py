from modules.users import User, UserRegistrationRequest
from typing import Optional
import base64
from percistance.connections import read_query, insert_query
from percistance.data import session_store
from percistance.queries import ALL_USERS, USER_BY_ID, USER_BY_EMAIL, USER_BY_USERNAME, NEW_USER, LOGIN_USERNAME_PASS


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
    usernm = read_query(USER_BY_USERNAME, (username,))
    userem = read_query(USER_BY_EMAIL, (email,))
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
    user = read_query(LOGIN_USERNAME_PASS, (username, password))
    if not user:
        raise ValueError(f'User with email {username} does not exist.')

    if user[0][2] != password:
        raise ValueError('The provided password is incorrect! Please try again.')
    # assign user_id, username and user_role
    token = encode(user[0][0], user[0][1], user[0][3])
    session_store["bearer"] = token

    return {"token": token, "token_type": "bearer"}


def un_authenticate_user(username: str):
    user = get_user_by_username(username)
    if not user:
        raise ValueError(f'User {username} is not logged in.')
    session_store["bearer"] = ""
    return {"message": f"User {username} successfully logged out."}


def authenticate(authorization) -> bool:
    if not authorization or authorization != session_store.get("bearer"):
        return False
    return True


def authorise_user_role(token: str):
    user = session_store.get("bearer")
    if not user:
        raise ValueError("Invalid session or expired token")
    result = decode(token)

    return result


def encode(user_id: int, username: str, user_role: int) -> str:
    user_string = f"{user_id}_{username}_{user_role}"
    encoded_bytes = base64.b64encode(user_string.encode('utf-8'))

    return encoded_bytes.decode('utf-8')

def decode(encoded_value: str):
    decoded_string = base64.b64decode(encoded_value).decode('utf-8')
    user_id, username, user_role = decoded_string.split('_')
    result = {
        "user_id": int(user_id),
        "username": username,
        "user_role": int(user_role)
    }
    return result