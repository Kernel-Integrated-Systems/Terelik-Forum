from pydantic import BaseModel
from typing import List
from modules.replies import Reply

class Topic(BaseModel):
    topic_id: int
    title: str
    content: str
    user_id: int
    category_id: int
    replies: List[Reply] = []


    @classmethod
    def view_topics(cls, topic_id, title, content, user_id, category_id, replies):
        return cls(
            topic_id=topic_id,
            title=title,
            content=content,
            user_id=user_id,
            category_id=category_id,
            replies=replies
        )


class NewTopic(BaseModel):
    title: str
    content: str
    user_id: int
    category_id: int
