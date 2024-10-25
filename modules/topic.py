from pydantic import BaseModel

class Topic(BaseModel):
    topic_id: int
    title: str
    content: str
    user_id: int
    category_id: int
    is_locked: int


    @classmethod
    def view_topics(cls, topic_id, title, content, user_id, category_id, is_locked):
        return cls(topic_id=topic_id, title=title, content=content, user_id=user_id, category_id=category_id,
                   is_locked=is_locked)


class NewTopic(BaseModel):
    title: str
    content: str
    user_id: int
    category_id: int
