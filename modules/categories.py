from pydantic import BaseModel


class Category(BaseModel):
    category_id: int | None = None
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
