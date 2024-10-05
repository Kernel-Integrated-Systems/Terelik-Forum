from pydantic import BaseModel


class Message(BaseModel):
    message_id: int | None = None
    sender_id: int
    receiver_id: int
    content: str

