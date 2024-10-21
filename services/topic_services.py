
from modules.topics import Topics
from percistance.connections import read_query, insert_query, update_query
from percistance.queries import ALL_TOPICS, TOPIC_BY_ID, TOPIC_BY_TITLE, TOPIC_BY_CATEGORY, NEW_TOPIC, DELETE_TOPIC


def view_topics():
    data = read_query(ALL_TOPICS)
    return (Topics.view_topics(*row) for row in data)

def find_topic_by_id(id: int):
    data = read_query(TOPIC_BY_ID, (id,))
    if not data:
        raise ValueError(f'Topic with ID {id} does not exist.')
    return next((Topics.view_topics(*row) for row in data), None)

def find_topic_by_title(title: str):
    data = read_query(TOPIC_BY_TITLE, (title,))
    if not data:
        raise ValueError(f'Topic with title {title} does not exist.')
    return next((Topics.view_topics(*row) for row in data), None)


def find_topic_by_category(category_id: int):
    data = read_query(TOPIC_BY_CATEGORY, (category_id,))
    if not data:
        raise ValueError(f'There is no topic with category {category_id}.')
    return next((Topics.view_topics(*row) for row in data), None)


def create_topic(title: str, content: str, user_id: int, category: int):
    new_topic_id = insert_query(NEW_TOPIC, (title, content, user_id, category))

    return {"message": f"New topic ID {new_topic_id} with title {title} is created at {category}."}

def remove_topic(topic_id: int):
    find_topic_by_id(topic_id)
    update_query(DELETE_TOPIC, (topic_id,))
    return {"message": f"Topic with ID {topic_id} is successfully deleted."}
