from modules.categories import Category
from percistance.connections import read_query, insert_query, update_query
from percistance.queries import ALL_CATEGORIES, CATEGORY_BY_ID, NEW_CATEGORY, DELETE_CATEGORY


def view_categories():
    data = read_query(ALL_CATEGORIES)
    return (Category.from_query_string(*row) for row in data)


def find_category_by_id(category_id: int):
    data = read_query(CATEGORY_BY_ID, (category_id,))
    if not data:
        raise ValueError(f'Category with ID {category_id} does not exist.')
    for r in data:
        print(r)
    return next((Category.from_query_string(*row) for row in data), None)


def create_category(title: str):
    new_id = insert_query(NEW_CATEGORY, (title,))
    return {"message": f"New Category {title} created with ID {new_id}."}


def remove_category(category_id: int):
    find_category_by_id(category_id,)
    update_query(DELETE_CATEGORY, (category_id,))
    return {"message": f"Category with ID {category_id} is successfully deleted."}


def grant_read_access(user_id: int, category_id: int):
    query = """INSERT INTO UserCategoryAccess (user_id, category_id, access_level) 
               VALUES (?, ?, 1) 
               ON CONFLICT(user_id, category_id) DO UPDATE SET access_level = 1"""
    insert_query(query, (user_id, category_id))
    return {"message": f"User {user_id} granted read access to category {category_id}"}

def user_has_access(user_id: int, category_id: int, required_access: int):
    query = """SELECT access_level FROM UserCategoryAccess 
               WHERE user_id = ? AND category_id = ?"""
    data = read_query(query, (user_id, category_id))
    if not data:
        return False
    access_level = data[0][0]
    if required_access == 1 and access_level in [1, 2]:
        return True
    elif required_access == 2 and access_level == 2:
        return True
    return False