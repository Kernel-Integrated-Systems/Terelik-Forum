from pydantic import BaseModel


class Category(BaseModel):
    category_id: int
    category_name: str
