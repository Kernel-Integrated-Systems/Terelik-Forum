from modules.categories import Category
from percistance.connections import read_query, insert_query, update_query
from percistance.queries import ALL_CATEGORIES, CATEGORY_BY_ID, NEW_CATEGORY, DELETE_CATEGORY


def view_categories(is_locked: bool = None):
    query = ALL_CATEGORIES
    params = ()
    if is_locked is not None:
        query += " WHERE is_locked = ?"
        params = (is_locked,)

    data = read_query(query, params)
    # Ensure each row has five elements (category_id, category_name, is_private, is_locked, created_at)
    return (Category.from_query_string(*row) for row in data)

def find_category_by_id(category_id: int):
    data = read_query(CATEGORY_BY_ID, (category_id,))
    if not data:
        raise ValueError(f'Category with ID {category_id} does not exist.')
    for r in data:
        print(r)
    return next((Category.from_query_string(*row) for row in data), None)


def create_category(title: str, private, locked):
    # Check if a category with the same name already exists
    existing_category = read_query("SELECT * FROM categories WHERE category_name = ?", (title,))
    if existing_category:
        raise ValueError(f"A category with the name '{title}' already exists.")

    is_private = int(private)
    is_locked = int(locked)

    new_id = insert_query(NEW_CATEGORY, (title, is_private, is_locked))
    return {"message": f"New Category '{title}' created with ID {new_id}."}


def remove_category(category_id: int):
    find_category_by_id(category_id,)
    update_query(DELETE_CATEGORY, (category_id,))
    return {"message": f"Category with ID {category_id} is successfully deleted."}

