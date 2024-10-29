from modules.topic import Topic
from modules.replies import Reply
from percistance.connections import read_query, insert_query, update_query
from percistance import queries

def view_topics():
    topic_data = read_query(queries.ALL_TOPICS)
    topics = []
    for row in topic_data:
        topic_id, title, content, user_id, category_id = row

        reply_data = read_query(queries.REPLIES_FOR_TOPIC, (topic_id,))
        replies = [
            Reply(
                reply_id=reply_row[0],
                content=reply_row[1],
                user_id=reply_row[2],
                topic_id=reply_row[3],
                created_at=reply_row[4]
            ) for reply_row in reply_data
        ]

        topic = Topic.view_topics(
            topic_id=topic_id,
            title=title,
            content=content,
            user_id=user_id,
            category_id=category_id,
            replies=replies
        )
        topics.append(topic)
    return topics


def find_topic_by_id(id: int):
    topic_data = read_query(queries.TOPIC_BY_ID, (id,))
    if not topic_data:
        raise ValueError(f'Topic with ID {id} does not exist.')

    for row in topic_data:
        topic_id, title, content, user_id, category_id = row

        reply_data = read_query(queries.REPLIES_FOR_TOPIC, (topic_id,))
        replies = [
            Reply(
                reply_id=reply_row[0],
                content=reply_row[1],
                user_id=reply_row[2],
                topic_id=reply_row[3],
                created_at=reply_row[4]
            ) for reply_row in reply_data
        ]

        return Topic.view_topics(
            topic_id=topic_id,
            title=title,
            content=content,
            user_id=user_id,
            category_id=category_id,
            replies=replies
        )


def find_topic_by_title(title: str):
    data = read_query(queries.TOPIC_BY_TITLE, (title,))
    if not data:
        raise ValueError(f'Topic with title {title} does not exist.')
    return next((Topic.view_topics(*row) for row in data), None)


def find_topic_by_category(category_id: int):
    data = read_query(queries.TOPIC_BY_CATEGORY, (category_id,))
    if not data:
        raise ValueError(f'There is no topic with category {category_id}.')
    return next((Topic.view_topics(*row) for row in data), None)


def create_topic(title: str, content: str, user_id: int, category: int):
    new_topic_id = insert_query(queries.NEW_TOPIC, (title, content, user_id, category))
    return Topic(topic_id=new_topic_id, title=title, content=content, user_id=user_id, category_id=category)


def remove_topic(topic_id: int):
    find_topic_by_id(topic_id)
    update_query(queries.DELETE_TOPIC, (topic_id,))
    return {"message": f"Topic with ID {topic_id} is successfully deleted."}


def change_topic_lock_status(topic_id: int):
    topic = find_topic_by_id(topic_id)
    if not topic:
        raise ValueError(f'There is no topic with ID {topic_id}.')
    if topic.is_locked == 0:
        updated_topics = 1
        update_query(queries.CHANGE_TOPIC_LOCK_STATUS, (updated_topics, topic_id,))
        return {"message": f"Topic with ID {topic_id} is successfully locked."}
    if topic.is_locked == 1:
        updated_topics = 0
        update_query(queries.CHANGE_TOPIC_LOCK_STATUS, (updated_topics, topic_id,))
        return {"message": f"Topic with ID {topic_id} is successfully unlocked."}


def check_topic_lock_status(topic_id: int):
    data = read_query(queries.CHANGE_TOPIC_LOCK_STATUS, (topic_id,))
    return data