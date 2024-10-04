from pydantic import BaseModel

class Topics(BaseModel):
    topic_id: int
    title: str
    category: str

