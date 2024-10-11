from pydantic import BaseModel

class Topics(BaseModel):
    topic_id: int
    title: str
    content: str
    user_id: int
    category_id: int

    @classmethod
    def view_topics(cls, topic_id, title, content, user_id, category_id):
        return cls(topic_id=topic_id, title=title, content=content, user_id=user_id, category_id=category_id)

