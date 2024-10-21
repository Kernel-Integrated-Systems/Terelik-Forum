from pydantic import BaseModel


class Message(BaseModel):
    message_id: int | None = None
    sender_id: int
    sender: str | None = None
    receiver_id: int
    receiver: str | None = None
    content: str

    @classmethod
    def from_query_string(cls, message_id, sender_id, sender, receiver_id, receiver, content):
        return cls(
            message_id=message_id,
            sender_id=sender_id,
            sender=sender,
            receiver_id=receiver_id,
            receiver=receiver,
            content=content
        )


class NewMessage(BaseModel):
    sender_id: int
    receiver_id: int
    content: str

class NewMessageRespond(BaseModel):
    sender: str
    receiver: str
    content: str

    @classmethod
    def from_query_string(cls, sender, receiver, content):
        return cls(
            sender=sender,
            receiver=receiver,
            content=content
        )
