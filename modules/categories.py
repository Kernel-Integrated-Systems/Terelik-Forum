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