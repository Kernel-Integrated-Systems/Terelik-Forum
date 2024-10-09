from modules.messages import Message
from percistance.data import messages


def get_messages(current_user_id: int):
    return [m for m in messages if m.sender_id == current_user_id]


def get_message_by_id(current_user_id: int, target_user_id: int):
    target_messages = next((m for m in messages if m.message_id == current_user_id and m.sender_id == target_user_id), None)
    return list(target_messages)

