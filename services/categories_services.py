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
    return (Category.from_query_string(*row) for row in data)


def find_category_by_id(category_id: int):
    data = read_query(CATEGORY_BY_ID, (category_id,))
    if not data:
        raise ValueError(f'Category with ID {category_id} does not exist.')
    for r in data:
        print(r)
    return next((Category.from_query_string(*row) for row in data), None)



def create_category(title: str, is_private, is_locked):
    # Update the insert query to include is_private and is_locked fields
    new_id = insert_query(NEW_CATEGORY, (title, int(is_private), int(is_locked)))
    return {"message": f"New Category '{title}' created with ID {new_id}."}
def remove_category(category_id: int):
    find_category_by_id(category_id,)
    update_query(DELETE_CATEGORY, (category_id,))
    return {"message": f"Category with ID {category_id} is successfully deleted."}

