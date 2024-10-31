from modules.categories import Category, CategoryPrivilegedUsersResponse, Categories, NewCategory
from modules.topic import Topics
from percistance.queries import ALL_CATEGORIES, CATEGORY_BY_ID, NEW_CATEGORY, DELETE_CATEGORY, CATEGORY_BY_NAME, \
    CATEGORY_PRIVILEGED_USERS, TOPICS_FOR_CATEGORY
from percistance.connections import read_query, insert_query, update_query



def view_categories():
    data = read_query(ALL_CATEGORIES)
    return (Categories.from_query_string(*row) for row in data)


def find_category_by_id(category_id: int):
    data = read_query(CATEGORY_BY_ID, (category_id,))
    if not data:
        raise ValueError(f'Category with ID {category_id} does not exist.')

    category_id, category_name, private, locked = data[0]

    topic_data = read_query(TOPICS_FOR_CATEGORY, (category_id,))
    topics = [
        Topics(
            topic_id=topic_row[0],
            title=topic_row[1],
            content=topic_row[2],
            user_id=topic_row[3],
            category_id=topic_row[4],
            is_locked=topic_row[5]
        ) for topic_row in topic_data
    ]

    category = Category.from_query_string(
        category_id=category_id,
        category_name=category_name,
        private=private,
        locked=locked,
        topics=topics
    )

    return category


def find_category_by_name(category_name: str):
    data = read_query(CATEGORY_BY_NAME, (category_name,))

    return next((Categories.from_query_string(*row) for row in data), None)



def create_category(title: str, private: int | None = None, locked: int | None = None):
    does_exist = find_category_by_name(title)

    if does_exist:
        raise ValueError(f'Category with name {title} already exists!')

    new_id = insert_query(NEW_CATEGORY, (title,))

    # Update category details if provided
    private = private if isinstance(private, int) else 0
    locked = locked if isinstance(locked, int) else 0
    #update_query(NEW_CATEGORY_DETAILS, (private, locked, new_id))
    update_query(NEW_CATEGORY, (private, locked, new_id))

    new_category = NewCategory(id=new_id, category_name=title, private=private, locked=locked)

    return new_category


def remove_category(category_id: int):
    find_category_by_id(category_id,)
    update_query(DELETE_CATEGORY, (category_id,))
    return {"message": f"Category with ID {category_id} is successfully deleted."}


def show_users_on_category(category_id: int):
    data = read_query(CATEGORY_PRIVILEGED_USERS, (category_id,))
    if not data:
        raise ValueError(f'The category with ID {category_id} is not private!')
    return (CategoryPrivilegedUsersResponse.from_query_string(*row) for row in data)

