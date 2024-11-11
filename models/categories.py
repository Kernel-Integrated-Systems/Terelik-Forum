from pydantic import BaseModel
from typing import List, Optional
from models.topic import Topics


class Categories(BaseModel):
    category_id: int | None = None
    category_name: str
    private: int | None = None
    locked: int | None = None
    topic_count: Optional[int] = 0
    reply_count: Optional[int] = 0

    @classmethod
    def from_query_string(cls, category_id, category_name, private, locked):
        return cls(
            category_id=category_id,
            category_name=category_name,
            private=private,
            locked=locked,

        )



class Category(BaseModel):
    category_id: int | None = None
    category_name: str
    private: int | None = None
    locked: int | None = None
    topics: List[Topics] = []

    @classmethod
    def from_query_string(cls, category_id, category_name, private, locked, topics=None):
        return cls(
            category_id=category_id,
            category_name=category_name,
            private=private,
            locked=locked,
            topics=topics if topics else []
        )

class NewCategory(BaseModel):
    category_name: str
    private: bool = False
    locked: bool = False


class CategoryPrivilegedUsersResponse(BaseModel):
    category_id: int
    category_name: str
    username: str
    access: str

    @classmethod
    def from_query_string(cls, category_id, category_name, username, access):
        return cls(
            category_id=category_id,
            category_name=category_name,
            username=username,
            access=access
        )
