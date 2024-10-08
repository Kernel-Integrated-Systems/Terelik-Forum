from modules.messages import Message
from percistance.data import messages
from services.user_services import get_user_by_id


def get_messages(current_user_id: int):
    return [m for m in messages if m.sender_id == current_user_id]


def get_message_by_id(current_user_id: int, target_user_id: int):
    target_messages = next((m for m in messages if m.sender_id == current_user_id and m.receiver_id == target_user_id), None)
    return target_messages


def create_message(message_content: Message) -> Message:
    new_id = max(m.message_id for m in messages) + 1 if messages else 1
    new_message = Message(message_id=new_id, **message_content.dict(exclude={'message_id'}))
    messages.append(new_message)
    return new_message


def post_new_message(sender: int, receiver: int, text: str):
    if not get_user_by_id(sender):
        raise ValueError(f"Sender with ID {sender} does not exist!")
    if not get_user_by_id(receiver):
        raise ValueError(f"Receiver with ID {receiver} does not exist!")
    if len(text) < 1:
        raise ValueError(f"Message content cannot be empty!")

    message_context = Message(sender_id=sender, receiver_id=receiver, content=text)

    return create_message(message_context)
