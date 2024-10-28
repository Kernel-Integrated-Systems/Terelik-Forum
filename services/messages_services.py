from modules.messages import Message, NewMessage, NewMessageRespond
from percistance.connections import read_query, insert_query
from percistance.queries import ALL_MESSAGES, MESSAGE_BY_ID, NEW_MESSAGE
from services.user_services import get_user_by_id


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


def create_message(message_content: NewMessage):
    new_id = insert_query(NEW_MESSAGE,
                          (message_content.sender_id,
                           message_content.receiver_id,
                           message_content.content))
    sender = message_content.sender_id
    receiver = message_content.receiver_id
    content = message_content.content
    return {"message": f"New message ID {new_id} sent FROM {sender} TO {receiver} with content < {content} >."}


def post_new_message(sender: int, receiver: int, text: str):
    if not get_user_by_id(sender):
        raise ValueError(f"Sender with ID {sender} does not exist!")
    if not get_user_by_id(receiver):
        raise ValueError(f"Receiver with ID {receiver} does not exist!")
    if len(text) < 1:
        raise ValueError(f"Message content cannot be empty!")

    message_context = NewMessage(sender_id=sender, receiver_id=receiver, content=text)

    return create_message(message_context)
