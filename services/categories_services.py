from modules.categories import Category, NewCategory
from percistance.connections import read_query, insert_query, update_query
from percistance.queries import (ALL_CATEGORIES, CATEGORY_BY_ID, NEW_CATEGORY, DELETE_CATEGORY,
                                 CATEGORY_BY_NAME, CHANGE_CATEGORY_PRIVATE, CHANGE_CATEGORY_LOCK_STATUS)
from percistance import queries

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


def find_category_by_name(category_name: str):
    data = read_query(CATEGORY_BY_NAME, (category_name,))

    return next((Category.from_query_string(*row) for row in data), None)

def create_category(title: str):
    does_exist = find_category_by_name(title)
    if does_exist:
        raise ValueError(f'Category with name {title} already exists!')
    new_id = insert_query(NEW_CATEGORY, (title,))
    new_category = NewCategory(id=new_id,category_name=title)
    return new_category


def remove_category(category_id: int):
    find_category_by_id(category_id,)
    update_query(DELETE_CATEGORY, (category_id,))
    return {"message": f"Category with ID {category_id} is successfully deleted."}


def change_category_private_status(category_id: int):
    category = find_category_by_id(category_id,)

    if category.private == 0:
        updated_category = 1
        update_query(CHANGE_CATEGORY_PRIVATE, (updated_category, category_id,))
        return {"message": f"Category with ID {category_id} is successfully changed to private."}
    elif category.private == 1:
        updated_category = 0
        update_query(CHANGE_CATEGORY_PRIVATE, (updated_category, category_id,))
        return {"message": f"Category with ID {category_id} is successfully changed to non-private."}


def change_category_lock_status(category_id: int):
    category = find_category_by_id(category_id,)
    if category.locked == 0:
        updated_category = 1
        update_query(CHANGE_CATEGORY_LOCK_STATUS, (updated_category, category_id,))
        return {"message": f"Category with ID {category_id} is successfully locked."}
    if category.locked == 1:
        updated_category = 0
        update_query(CHANGE_CATEGORY_LOCK_STATUS, (updated_category, category_id,))
        return {"message": f"Category with ID {category_id} is successfully unlocked."}


def check_category_lock_status(category_id: int):
    data = read_query(queries.CHECK_CATEGORY_PRIVATE_STATUS, (category_id,))
    return data