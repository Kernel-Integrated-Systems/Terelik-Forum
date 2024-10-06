from pydantic import BaseModel

class Topics(BaseModel):
    topic_id: int
    title: str
    content: str
    user_id: int
    category_id: int