from modules.messages import Message, NewMessage, NewMessageRespond
from percistance.connections import read_query, insert_query
from percistance.queries import ALL_MESSAGES, MESSAGE_BY_ID, NEW_MESSAGE
from services.user_services import get_user_by_id
from datetime import datetime

def get_messages(current_user_id: int):
    data = read_query(ALL_MESSAGES, (current_user_id, current_user_id))
    if not data:
        raise ValueError(f'There are no message exchanges with user ID {current_user_id}!')
    return (NewMessageRespond.from_query_string(*row) for row in data)


def get_message_by_id(current_user_id: int, target_user_id: int):
    msg_data = read_query(MESSAGE_BY_ID, (current_user_id, target_user_id))
    if not msg_data:
        raise ValueError(f'There are no messages between user {current_user_id} and user {target_user_id}!')
    return (NewMessageRespond.from_query_string(*row) for row in msg_data)


def create_message(sender_id: int, receiver_id: int, content: str):
    return insert_query(NEW_MESSAGE, (sender_id,receiver_id,content))


def post_new_message(message_id: int, sender: str, receiver: str, text: str):
    if len(text) < 1:
        raise ValueError("Message content cannot be empty!")
    stamp = datetime.now()
    msg_response = NewMessageRespond(message_id=message_id, sent_at=stamp, sender=sender, receiver=receiver, content=text)
    return msg_response