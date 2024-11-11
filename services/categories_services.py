from models.categories import Categories, Category, CategoryPrivilegedUsersResponse, NewCategory
from models.topic import Topics
from percistance.connections import read_query, insert_query, update_query
from percistance import queries


def search_categories(query: str):
    data = read_query("SELECT * FROM categories WHERE category_name LIKE ?", (f"%{query}%",))
    return [Categories.from_query_string(*row) for row in data]
def count_topics(category_id: int) -> int:
    topic_data = read_query(queries.TOPICS_FOR_CATEGORY, (category_id,))
    return len(topic_data)

def count_replies(category_id: int):
    topic_data = read_query(queries.TOPICS_FOR_CATEGORY, (category_id,))
    reply_count = 0
    for topic in topic_data:
        topic_id = topic[0]
        replies = read_query(queries.REPLIES_FOR_TOPIC, (topic_id,))
        reply_count += len(replies)
    return reply_count

def view_categories():
    data = read_query(queries.ALL_CATEGORIES)
    categories = [Categories.from_query_string(*row) for row in data]
    for category in categories:
        category.topic_count = count_topics(category.category_id)
        category.reply_count = count_replies(category.category_id)
    return categories


def count_topics_per_category():
    topic_counts = read_query("""
        SELECT category_id, COUNT(topic_id) AS topic_count
        FROM topics
        GROUP BY category_id
    """)
    return {row[0]: row[1] for row in topic_counts}
def count_replies_per_category():
    reply_counts = read_query("""
        SELECT t.category_id, COUNT(r.reply_id) AS reply_count
        FROM topics t
        LEFT JOIN replies r ON t.topic_id = r.topic_id
        GROUP BY t.category_id
    """)
    return {row[0]: row[1] for row in reply_counts}

def find_category_by_id(category_id: int):
    data = read_query(queries.CATEGORY_BY_ID, (category_id,))
    if not data:
        raise ValueError(f'Category with ID {category_id} does not exist.')

    category_id, category_name, private, locked = data[0]

    topic_data = read_query(queries.TOPICS_FOR_CATEGORY, (category_id,))
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
    data = read_query(queries.CATEGORY_BY_NAME, (category_name,))

    return next((Categories.from_query_string(*row) for row in data), None)


def create_category(
        title: str,
        private: int | None = None,
        locked: int | None = None):
    does_exist = find_category_by_name(title)
    if does_exist:
        raise ValueError(f'Category with name {title} already exists!')

    new_id = insert_query(queries.NEW_CATEGORY, (title,))

    update_query(queries.NEW_CATEGORY_DETAILS, (private, locked, new_id))
    new_category = NewCategory(id=new_id,category_name=title, private=private, locked=locked)

    return new_category


def remove_category(category_id: int):
    find_category_by_id(category_id,)
    update_query(queries.DELETE_CATEGORY, (category_id,))
    return {"message": f"Category with ID {category_id} is successfully deleted."}


def show_users_on_category(category_id: int):
    data = read_query(queries.CATEGORY_PRIVILEGED_USERS, (category_id,))
    if not data:
        raise ValueError(f'The category with ID {category_id} is not private!')
    return (CategoryPrivilegedUsersResponse.from_query_string(*row) for row in data)
