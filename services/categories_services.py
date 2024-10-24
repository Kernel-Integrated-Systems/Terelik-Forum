from modules.categories import Category, NewCategory
from percistance.connections import read_query, insert_query, update_query
from percistance.queries import ALL_CATEGORIES, CATEGORY_BY_ID, NEW_CATEGORY, DELETE_CATEGORY, CATEGORY_BY_NAME


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
