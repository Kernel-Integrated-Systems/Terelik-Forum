from fastapi import APIRouter, Response, HTTPException

from modules.messages import NewMessage
from services.message_services import get_messages, get_message_by_id, post_new_message
from services.user_services import authenticate

messages_router = APIRouter(prefix='/messages', tags=['Messages'])


# View Conversations - regardless of receiver
@messages_router.get("/{user_id}")
def get_user_messages(user_id: int, token: str | None = None):
    if not authenticate(token):
        raise HTTPException(status_code=401, detail="Authorization token missing or invalid")

    try:
        return get_messages(user_id)
    except ValueError as e:
        return Response(status_code=400, content=str(e))

# View Conversation - to a particular receiver
@messages_router.get("/{user_id}/{target_usr_id}")
def get_user_message(user_id: int, target_usr_id: int, token: str | None = None):
    if not authenticate(token):
        raise HTTPException(status_code=401, detail="Authorization token missing or invalid")

    try:
        return get_message_by_id(user_id, target_usr_id)
    except ValueError as e:
        return Response(status_code=400, content=str(e))


# Create New Message
@messages_router.post("/")
def create_new_message(user: NewMessage, token: str | None = None):
    if not authenticate(token):
        raise HTTPException(status_code=401, detail="Authorization token missing or invalid")

    try:
        new_message = post_new_message(sender=user.sender_id,receiver=user.receiver_id,text=user.content)
        return new_message
    except ValueError as e:
        return Response(status_code=400, content=str(e))
