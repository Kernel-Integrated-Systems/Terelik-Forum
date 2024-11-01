from pydantic import BaseModel
from typing import List
from modules.replies import Reply

class Topics(BaseModel):
    topic_id: int
    title: str
    content: str
    user_id: int
    category_id: int
    is_locked: int

    @classmethod
    def from_query_string(cls, topic_id, title, content, user_id, category_id, is_locked):
        return cls(
            topic_id=topic_id,
            title=title,
            content=content,
            user_id=user_id,
            category_id=category_id,
            is_locked=is_locked
        )


class Topic(BaseModel):
    topic_id: int
    title: str
    content: str
    user_id: int
    category_id: int
    is_locked: int = 0
    replies: List[Reply] = []


    @classmethod
    def from_query_string(cls, topic_id, title, content, user_id, category_id, is_locked, replies):
        return cls(
            topic_id=topic_id,
            title=title,
            content=content,
            user_id=user_id,
            category_id=category_id,
            is_locked=is_locked,
            replies=replies
        )


class NewTopic(BaseModel):
    title: str
    content: str
    user_id: int
    category_id: int
