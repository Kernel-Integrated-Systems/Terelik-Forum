from modules.topic import Topic, Topics
from modules.replies import Reply, BestReply
from percistance.connections import read_query, insert_query, update_query
from percistance import queries


# View Topics
def view_topics(search: str = None, page: int = 1, page_size: int = 4):
    topic_data = read_query(queries.ALL_TOPICS)
    # Apply search query
    if search:
        filtered_topics = [
            Topics.from_query_string(*row)
            for row in topic_data
            if any(word.lower() == search.lower() for word in row[1].split())
        ]
    else:
        filtered_topics = [Topics.from_query_string(*row) for row in topic_data]

    # Implement pagination
    start_index = (page - 1) * page_size
    end_index = start_index + page_size
    paginated_topics = filtered_topics[start_index:end_index]

    return paginated_topics


def sort_topics(topics: list[Topics], attribute='title', reverse=False):
    if attribute == 'title':
        sort_key = lambda t: t.title
    elif attribute == 'is_locked':
        sort_key = lambda t: t.is_locked
    else:
        sort_key = lambda t: t.topic_id

    return sorted(topics, key=sort_key, reverse=reverse)

# Topic Response helper
def get_topic_with_replies(topic_data):

    topic_id, title, content, user_id, category_id, is_locked = topic_data[0]

    # Retrieve replies for the topic
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

    # Create the Topic instance with replies
    topic = Topic.from_query_string(
        topic_id=topic_id,
        title=title,
        content=content,
        user_id=user_id,
        category_id=category_id,
        is_locked=is_locked,
        replies=replies
    )

    return topic

# Find Topic by ID
def find_topic_by_id(topic_id: int):
    topic_data = read_query(queries.TOPIC_BY_ID, (topic_id,))
    if not topic_data:
        raise ValueError(f'Topic with ID {topic_id} does not exist.')

    return get_topic_with_replies(topic_data)

def find_topic_by_title(title: str):
    topic_data = read_query(queries.TOPIC_BY_TITLE, (title,))
    if not topic_data:
        raise ValueError(f'Topic with title {title} does not exist.')

    return get_topic_with_replies(topic_data)


def find_topic_by_category(category_id: int):
    topic_data = read_query(queries.TOPIC_BY_CATEGORY, (category_id,))
    if not topic_data:
        raise ValueError(f'There is no topic with category {category_id}.')

    return get_topic_with_replies(topic_data)

# Post Topic
def create_topic(title: str, content: str, user_id: int, category: int, is_locked: int):
    new_topic_id = insert_query(queries.NEW_TOPIC, (title, content, user_id, category, is_locked))
    return Topic(topic_id=new_topic_id, title=title, content=content, user_id=user_id, category_id=category, is_locked=0)

# Choose Best Reply on Topic
def choose_best_reply(topic_id: int, reply_id: int, user_id: int):
    topic = find_topic_by_id(topic_id)
    replies = topic.replies
    if not topic:
        raise ValueError("Topic not found.")
    if topic.user_id != user_id:
        raise ValueError("Only the topic author can select the best reply.")

    reply_ids = [reply.reply_id for reply in replies]
    if reply_id not in reply_ids:
        raise ValueError("There is no such reply for this topic!")

    update_query(queries.ADD_BEST_REPLY_ON_TOPIC, (reply_id, topic_id))

    return BestReply(topic_id=topic_id, reply_id=reply_id)


def remove_topic(topic_id: int):
    find_topic_by_id(topic_id)
    update_query(queries.DELETE_TOPIC, (topic_id,))
    return {"message": f"Topic with ID {topic_id} is successfully deleted."}


def change_topic_lock_status(topic_id: int):
    topic = find_topic_by_id(topic_id)[0]
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
    data = read_query(queries.CHECK_TOPIC_PRIVATE_STATUS, (topic_id,))
    if not data:
        return None
    return data[0][0]
