from fastapi import APIRouter, Response, HTTPException, Header
from modules.messages import NewMessage
from services.message_services import get_messages, get_message_by_id, post_new_message, create_message
from services.user_services import authenticate, get_user_by_id

messages_router = APIRouter(prefix='/api/messages', tags=['Messages'])


# View Conversations - regardless of receiver
@messages_router.get("/{user_id}")
def get_user_messages(user_id: int, token: str | None = Header()):
    # Check if user is authenticated
    user_data = authenticate(token)
    if not user_data:
        raise HTTPException(status_code=401, detail="Authorization token missing or invalid")
    try:
        return get_messages(user_id)
    except ValueError as e:
        return Response(status_code=400, content=str(e))

# View Conversation - to a particular receiver
@messages_router.get("/{user_id}/{target_usr_id}")
def get_user_message(user_id: int, target_usr_id: int, token: str | None = Header()):
    # Check if user is authenticated
    user_data = authenticate(token)
    if not user_data:
        raise HTTPException(status_code=401, detail="Authorization token missing or invalid")

    try:
        return get_message_by_id(user_id, target_usr_id)
    except ValueError as e:
        return Response(status_code=400, content=str(e))


# Create New Message
@messages_router.post("/")
def create_new_message(msg: NewMessage, token: str | None = Header()):
    # Check if user is authenticated
    user_data = authenticate(token)
    if not user_data:
        raise HTTPException(status_code=401, detail="Authorization token missing or invalid")

    sender = get_user_by_id(user_data["user_id"])
    if not sender:
        raise HTTPException(status_code=401, detail=f"Sender {sender.username} does not exist!")

    receiver = get_user_by_id(msg.receiver_id)
    if not receiver:
        raise HTTPException(status_code=401, detail=f"Receiver {receiver.username} does not exist!")

    try:
        message_id = create_message(sender_id=user_data["user_id"], receiver_id=receiver.id, content=msg.content)
        return post_new_message(message_id=message_id, sender=user_data["username"], receiver=receiver.username, text=msg.content)
    except ValueError as e:
        return Response(status_code=400, content=str(e))
