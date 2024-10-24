import base64
import datetime
from http.client import HTTPException

import jwt

from modules.users import User, UserRegistrationRequest
from typing import Optional

from percistance.connections import read_query, insert_query, update_query
from percistance.queries import ALL_USERS, USER_BY_ID, USER_BY_EMAIL, USER_BY_USERNAME, NEW_USER, LOGIN_USERNAME_PASS, \
    REMOVE_READ_ACCESS, REMOVE_WRITE_ACCESS



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



""" Аuthentication 
        Logic 
    and token JWT """

session_store = {}

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"

def create_jwt_token(user_id: int, username: str, user_role: int) -> str:
    expiration = datetime.datetime.utcnow() + datetime.timedelta(days=1)  # Token valid for 1 day
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
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

def authenticate(authorization: str) -> bool:
    if not authorization:
        return False
    token = authorization.split(" ")[1]
    try:
        decode_jwt_token(token)
        return True
    except ValueError:
        return False


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

# def blacklist_token(token: str):
#     query = "INSERT INTO blacklisted_tokens (token, blacklisted_at) VALUES (%s, %s)"
#     execute_query(query, (token, datetime.datetime.utcnow()))


def un_authenticate_user(token: str):
    try:
        # Decode the token ensure it's valid
        decoded_token = decode_jwt_token(token)
        username = decoded_token.get("username")

        # TODO IMPLEMENT token revocation by adding the token to a blacklist
        # (blacklist logic not implemented here)
        # blacklist.add(token)

        return {"message": f"User {username} successfully logged out."}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired.")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token.")


"""
Permissions for users - giving access 
"""

def grant_read_access(user_id: int, category_id: int):
    query = """INSERT INTO CategoryAccess (user_id, category_id, access_level) 
               VALUES (?, ?, 1) 
               ON CONFLICT(user_id, category_id) DO UPDATE SET access_level = 1"""
    insert_query(query, (user_id, category_id))
    return {"message": f"User {user_id} granted read access to category {category_id}"}

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

def grant_write_access(user_id: int, category_id: int):
    query = """
        INSERT INTO CategoryAccess (user_id, category_id, access_level) 
        VALUES (?, ?, 2) 
        ON CONFLICT(user_id, category_id) 
        DO UPDATE SET access_level = 2
    """
    insert_query(query, (user_id, category_id))
    return {"message": f"User {user_id} granted write access to category {category_id}"}


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

def logout_user(username: str):
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
