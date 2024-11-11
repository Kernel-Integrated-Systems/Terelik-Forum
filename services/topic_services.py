from models.categories import Category
from models.topic import Topic, Topics
from models.replies import Reply, BestReply
from percistance.connections import read_query, insert_query, update_query
from percistance import queries


# View Topics
def view_topics(search: str = None, page: int = 1, page_size: int = 4):
    topic_data = read_query(queries.ALL_TOPICS)

    if search:
        filtered_topics = [
            Topics.from_query_string(*row)
            for row in topic_data
            if any(word.lower() == search.lower() for word in row[1].split())
        ]
    else:
        filtered_topics = [Topics.from_query_string(*row) for row in topic_data]

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

def view_categories_with_topics():
    category_data = read_query("SELECT category_id, category_name, is_private, is_locked FROM Categories")
    categories = [Category.from_query_string(row[0], row[1], row[2], row[3]) for row in category_data]

    for category in categories:
        topics_data = read_query("SELECT topic_id, title, content, user_id, category_id, is_locked FROM Topics WHERE category_id = ?", (category.category_id,))
        topics = [Topics(topic_id=row[0], title=row[1], content=row[2], user_id=row[3], category_id=row[4], is_locked=row[5]) for row in topics_data]
        category.topics = topics
    return categories


# Find Topic by ID

def find_topic_by_category(category_id: int):
    data = read_query(queries.TOPIC_BY_CATEGORY, (category_id,))
    if not data:
        raise ValueError(f'There is no topic with category {category_id}.')

    topics = [Topic.from_query_string(*row) for row in data]
    return topics

def find_topic_by_id(topic_id: int):
    topic_data = read_query(
        "SELECT topic_id, title, content, user_id, category_id, is_locked FROM topics WHERE topic_id = ?",
        (topic_id,))
    if not topic_data:
        raise ValueError("Topic not found.")

    topic_id, title, content, user_id, category_id, is_locked = topic_data[0]

    replies_data = read_query("SELECT reply_id, content, user_id, topic_id FROM replies WHERE topic_id = ?",
                              (topic_id,))
    replies = [
        Reply(
            reply_id=row[0],
            content=row[1],
            user_id=row[2],
            topic_id=row[3]
        )
        for row in replies_data
    ]

    return Topic(
        topic_id=topic_id,
        title=title,
        content=content,
        user_id=user_id,
        category_id=category_id,
        is_locked=is_locked,
        replies=replies
    )


def find_topic_by_title(title: str):
    data = read_query(queries.TOPIC_BY_TITLE, (title,))
    if not data:
        raise ValueError(f'Topic with title {title} does not exist.')
    return next((Topic.from_query_string(*row) for row in data), None)



# Post Topic
def create_topic(title: str, content: str, user_id: int, category: int):
    new_topic_id = insert_query(queries.NEW_TOPIC, (title, content, user_id, category))
    return Topic(topic_id=new_topic_id, title=title, content=content, user_id=user_id, category_id=category)

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
    data = read_query("SELECT is_locked FROM topics WHERE topic_id = ?", (topic_id,))
    if not data:
        return None
    return data[0][0]
