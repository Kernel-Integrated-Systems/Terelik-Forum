import base64
from uuid import uuid4

from fastapi import HTTPException

session_store = {}


def authenticate(authorization) -> bool:
    if not authorization or authorization != session_store.get("bearer"):
        return False
    return True


def authorise_user_role(token: str):
    user = session_store.get(token)
    if not user:
        raise ValueError("Invalid session or expired token")
    _, username, user_role = decode(token)
    return user_role


def encode(user_id: int, username: str, user_role: int) -> str:
    user_string = f"{user_id}_{username}_{user_role}"
    encoded_bytes = base64.b64encode(user_string.encode('utf-8'))

    return encoded_bytes.decode('utf-8')

def decode(encoded_value: str):
    decoded_string = base64.b64decode(encoded_value).decode('utf-8')
    user_id, username, user_role = decoded_string.split('_')

    return {
        "user_id": int(user_id),
        "username": username,
        "user_role": int(user_role)
    }