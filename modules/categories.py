from pydantic import BaseModel


from pydantic import BaseModel


class Category(BaseModel):
    category_id: int | None = None
    category_name: str
    is_private: int | None = None
    is_locked: int | None = None

    @classmethod
    def from_query_string(cls, category_id, category_name, is_private, is_locked):
        return cls(
            category_id=category_id,
            category_name=category_name,
            is_private=is_private,
            is_locked=is_locked
        )


class NewCategory(BaseModel):
    category_name: str
    is_private: int = 0
    is_locked: int = 0