
from fastapi import APIRouter, Response, HTTPException, Header

from modules.messages import NewMessageRespond
from services.messages_services import get_messages, post_new_message, get_message_by_id
from services.user_services import authenticate, decode_jwt_token



messages_router = APIRouter(prefix='/messages', tags=['Messages'])


# View Conversations - regardless of receiver
@messages_router.get("/{user_id}")
def get_user_messages(user_id: int, authorization: str = Header(...)):
    user_info = authenticate(authorization)
    if user_info["user_id"] != user_id:
        raise HTTPException(status_code=403, detail="Access denied.")
    try:
        return get_messages(user_id)
    except ValueError as e:
        return Response(status_code=400, content=str(e))


# View Conversation - to a particular receiver
@messages_router.get("/{user_id}/{target_usr_id}")
def get_user_message(user_id: int, target_usr_id: int, authorization: str = Header(...)):
    user_info = authenticate(authorization)
    if user_info["user_id"] != user_id:
        raise HTTPException(status_code=403, detail="Access denied.")
    try:
        return get_message_by_id(user_id, target_usr_id)
    except ValueError as e:
        return Response(status_code=400, content=str(e))


# Create New Message
@messages_router.post("/")
def create_new_message(user=NewMessageRespond, authorization: str = Header(...)):
    user_info = authenticate(authorization)
    if user_info["user_id"] != user.sender:
        raise HTTPException(status_code=403, detail="You cannot send messages on behalf of another user.")
    try:
        new_message = post_new_message(sender=user.sender, receiver=user.receiver, text=user.content)
        return new_message
    except ValueError as e:
        return Response(status_code=400, content=str(e))
