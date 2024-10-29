
from fastapi import APIRouter, Response, HTTPException, Header

from modules.messages import NewMessage
from services.message_services import get_messages, post_new_message, get_message_by_id
from services.user_services import authenticate, decode




messages_router = APIRouter(prefix='/messages', tags=['Messages'])


# View Conversations - regardless of receiver
@messages_router.get("/{user_id}")
def get_user_messages(user_id: int, authorization: str = Header(...)):
    if not authenticate(authorization):
        raise HTTPException(status_code=401, detail="Authorization token missing or invalid")

    token_data = decode(authorization.split(" ")[1])
    if token_data["user_id"] != user_id:
        raise HTTPException(status_code=403, detail="Access denied.")
    try:
        return get_messages(user_id)
    except ValueError as e:
        return Response(status_code=400, content=str(e))


# View Conversation - to a particular receiver
@messages_router.get("/{user_id}/{target_usr_id}")
def get_user_message(user_id: int, target_usr_id: int, authorization: str = Header(...)):
    if not authenticate(authorization):
        raise HTTPException(status_code=401, detail="Authorization token missing or invalid")

    token_data = decode(authorization.split(" ")[1])
    if token_data["user_id"] != user_id:
        raise HTTPException(status_code=403, detail="Access denied.")
    try:
        return get_message_by_id(user_id, target_usr_id)
    except ValueError as e:
        return Response(status_code=400, content=str(e))


# Create New Message
@messages_router.post("/")
def create_new_message(message = NewMessage, authorization: str = Header(...)):
    token_data = authenticate(authorization)
    if not authenticate(authorization):
        raise HTTPException(status_code=401, detail="Authorization token missing or invalid")

    if token_data["user_id"] != message.sender_id:
        raise HTTPException(status_code=403, detail="You cannot send messages on behalf of another user.")
    try:
        new_message = post_new_message(sender=message.sender_id,receiver=message.receiver_id,text=message.content)
        return new_message
    except ValueError as e:
        return Response(status_code=400, content=str(e))
