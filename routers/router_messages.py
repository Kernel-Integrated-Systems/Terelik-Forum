from fastapi import APIRouter, Response

from services.message_services import get_messages, get_message_by_id, post_new_message

messages_router = APIRouter(prefix='/messages', tags=['Messages'])


# View Conversations - regardless of receiver
@messages_router.get("/{user_id}")
def get_user_messages(user_id: int):
    try:
        return get_messages(user_id)
    except ValueError as e:
        return Response(status_code=400, content=str(e))

# View Conversation - to a particular receiver
@messages_router.get("/{user_id}/{target_usr_id}")
def get_user_message(user_id: int, target_usr_id: int):
    try:
        return get_message_by_id(user_id, target_usr_id)
    except ValueError as e:
        return Response(status_code=400, content=str(e))


# Create New Message
@messages_router.post("/")
def create_new_message(sender_id: int, receiver_id: int, context: str):
    try:
        new_message = post_new_message(sender=sender_id,receiver=receiver_id,text=context)
        return new_message
    except ValueError as e:
        return Response(status_code=400, content=str(e))
