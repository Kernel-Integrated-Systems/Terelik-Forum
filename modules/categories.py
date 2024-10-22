from pydantic import BaseModel


class Category(BaseModel):
    category_id: int
    category_name: str
    private: int | None = None
    locked: int | None = None

    @classmethod
    def from_query_string(cls, category_id, category_name, private, locked):
        return cls(
            category_id=category_id,
            category_name=category_name,
            private=private,
            locked=locked
        )


class NewCategory(BaseModel):
    category_name: str
    private: int | None = None
    locked: int | None = None
