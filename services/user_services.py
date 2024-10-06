
from modules.users import User
from percistance.data import users
from typing import Optional


def get_all_users():
    return users


def get_user_by_id(user_id: int):
    return next((u for u in users if u.id == user_id), None)


def get_user_by_email(email: str) -> Optional[User]:
    for user in users:
        if user.email == email:
            return user
    return None


def get_user_by_username(username: str) -> Optional[User]:
    for user in users:
        if user.username == username:
            return user
    return None


def create_user(user_data: User) -> User:
    new_id = max(user.id for user in users) + 1 if users else 1
    print(new_id)
    new_user = User(id=new_id, **user_data.dict(exclude={'id'}))
    users.append(new_user)
    return new_user


def register_user(username: str, email: str, password: str) -> User:
    if get_user_by_username(username):
        raise ValueError('Username is already taken!')
    if get_user_by_email(email):
        raise ValueError('Email is already registered!')

    user_data = User(username=username, email=email, password=password, role='user', is_active=1)

    return create_user(user_data)


def authenticate_user(email: str, password: str) -> Optional[User]:
    user = get_user_by_email(email)
    if not user:
        return None

    if user.password != password:
        return None

    return user

