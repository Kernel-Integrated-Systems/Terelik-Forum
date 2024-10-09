from modules.categories import Category
from percistance.data import categories

def create_category(title: str):
    new_id = max(c.category_id for c in categories) + 1 if categories else 1
    new_category = Category(category_id=new_id, category_name=title)
    categories.append(new_category)
    return new_category


def view_categories():
    return categories


def find_category_by_id_f(category_id: int):
    for c in categories:
        if c.category_id == category_id:
            return c

