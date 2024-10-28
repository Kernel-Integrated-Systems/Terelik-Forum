import jwt
from fastapi import HTTPException
from modules.categories import Category
from modules.users import User, UserRegistrationRequest, UserAccess
from typing import Optional

from percistance.connections import read_query, insert_query, update_query
from percistance.queries import ALL_USERS, USER_BY_ID, USER_BY_EMAIL, USER_BY_USERNAME, NEW_USER, LOGIN_USERNAME_PASS, \
    REMOVE_READ_ACCESS, REMOVE_WRITE_ACCESS, GRANT_WRITE_ACCESS, GRANT_READ_ACCESS, GET_ACCESS_LEVEL

from datetime import datetime, timedelta


""" 
----------------------------------->
    Аuthentication 
        Logic 
    and token JWT 
----------------------------------->
"""

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"


def authenticate_user(username: str, password: str):
    user = read_query(LOGIN_USERNAME_PASS, (username, password))

    if not user:
        raise ValueError(f'User with username {username} does not exist.')

    if user[0][2] != password:
        raise ValueError('The provided password is incorrect! Please try again.')

    token = create_jwt_token(user[0][0], user[0][1], user[0][3])

    return {"token": token, "token_type": "bearer"}


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


def register_user(username: str, email: str, password: str):
    usernm = read_query(USER_BY_USERNAME, (username,))
    userem = read_query(USER_BY_EMAIL, (email,))
    if usernm:
        raise ValueError(f'Username {username} is already taken!')
    if userem:
        raise ValueError(f'Email is {email} already registered!')

    user_data = UserRegistrationRequest(username=username, email=email, password=password)
    new_user_id = create_user(user_data)



    token = create_jwt_token(new_user_id, username, 1)
    return {
        "user": {
            "id": new_user_id,
            "username": username,
            "email": email,
            "role": "user"
        },
        "token": token,
        "token_type": "bearer"
    }


def get_access_level(user_id: int, category_id: int):
    data = read_query(GET_ACCESS_LEVEL, (user_id, category_id))

    if not data:
        return None

    return data[0][0]

def logout_user(token: str):
  return {"message": "User successfully logged out. "}


"""
----------------------------------->
Permissions for users ACCESS LEVELS
----------------------------------->
"""


def grant_read_access(user_id: int, category_id: int) -> dict:
    user_access = UserAccess(user_id=user_id, category_id=category_id, access_level=1)
    insert_query(GRANT_READ_ACCESS, (user_access.user_id, user_access.category_id))
    return {"message": f"User {user_access.user_id} granted read access to category {user_access.category_id}"}


def grant_write_access(user_id: int, category_id: int, authorization: str) -> dict:
    if not authenticate(authorization):
        raise HTTPException(status_code=401, detail="Authorization token missing or invalid")

    token = authorization.split(" ")[1]
    user_info = decode_jwt_token(token)

    if user_info["user_role"] != 2:
        raise HTTPException(status_code=403, detail="You do not have permission to grant write access")

    user_access = UserAccess(user_id=user_id, category_id=category_id, access_level=2)
    insert_query(GRANT_WRITE_ACCESS, (user_access.user_id, user_access.category_id))
    return {"message": f"User {user_access.user_id} granted write access to category {user_access.category_id}"}


# def grant_write_access(user_id: int, category_id: int, authorization: str):
#     if not authenticate(authorization):
#         raise HTTPException(status_code=401, detail="Authorization token missing or invalid")
#
#     token = authorization.split(" ")[1]
#     user_info = decode_jwt_token(token)
#
#     if user_info["user_role"] != 2:
#         raise HTTPException(status_code=403, detail="You do not have permission to grant access")
#
#     insert_query(GRANT_WRITE_ACCESS, (user_id, category_id))
#     return {"message": f"User {user_id} granted write access to category {category_id}"}


def user_has_access(user_id: int, category_id: int, required_access: int):
    query = """SELECT access_level FROM UserCategoryAccess 
               WHERE user_id = ? AND category_id = ?"""
    data = read_query(query, (user_id, category_id))
    if not data:
        return False
    access_level = data[0][0]
    if required_access == 1 and access_level in [1, 2]:
        return True
    elif required_access == 2 and access_level == 2:
        return True
    return False


def get_user_accessible_categories(user_id: int):
    query = """
        SELECT c.category_id, c.category_name, c.is_private, c.is_locked
        FROM categories c
        JOIN CategoryAccess ca ON c.category_id = ca.category_id
        WHERE ca.user_id = ? AND c.is_locked = 1
    """
    data = read_query(query, (user_id,))

    # Ensure each row has five elements
    return (Category.from_query_string(*row) for row in data)


def revoke_access(user_id: int, category_id: int, access_type: str, authorization: str):

    if not authenticate(authorization):
        raise HTTPException(status_code=401, detail="Authorization token missing or invalid")

    token = authorization.split(" ")[1]
    user_info = decode_jwt_token(token)
    user_role = user_info["user_role"]

    if user_role != 2:
        raise HTTPException(status_code=403, detail="You do not have permission to revoke access")

    if access_type not in ["read", "write"]:
        raise HTTPException(status_code=400, detail="Invalid access type. Must be 'read' or 'write'.")

    if access_type == "read":
        result = update_query(REMOVE_READ_ACCESS, (user_id, category_id))
    elif access_type == "write":
        result = update_query(REMOVE_WRITE_ACCESS, (user_id, category_id))
    else:
        raise ValueError("Invalid access type. Must be 'read' or 'write'.")

    if result:
        return {"message": f"User {user_id}'s {access_type} access to category {category_id} has been revoked."}
    else:
        raise ValueError(f"Failed to revoke {access_type} access for user {user_id} to category {category_id}.")


def create_jwt_token(user_id: int, username: str, user_role: int) -> str:
    expiration = datetime.utcnow() + timedelta(days=1)  # Token valid for 1 day


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
        is_expired = payload['exp'] < datetime.utcnow().timestamp()
        return {
            "user_id": payload["user_id"],
            "username": payload["sub"],
            "user_role": payload["user_role"],
            "is_expired": is_expired
        }

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired.")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token.")


def authenticate(authorization: str) -> bool:
    if not authorization:
        return False

    token = authorization.split(" ")[1]
    decoded_token = decode_jwt_token(token)

    if decoded_token["is_expired"]:
        return False

    return True
