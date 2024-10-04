from modules.topics import Topics
from percistance.data import topics


def create_topic(topic_data: Topics):
    new_id = max(topic.topic_id for topic in topics) + 1 if topics else 1
    new_topic = Topics(id=new_id, **topic_data.dict())
    topics.append(new_topic)
    return new_topic


def view_topics():
    return topics


def find_topic_by_id(id: int):
    for topic in topics:
        if topic.topic_id == id:
            return topic


def find_topic_by_title(title: str):
    for topic in topics:
        if title.lower() == topic.title.lower():
            return topic


def find_topic_by_category(category: str):
    for topic in topics:
        if category.lower() in topic.category.lower():
            return topic


def post_new_topic(topic_id: int, title: str, category: str) -> Topics:
    if find_topic_by_title(title):
        raise ValueError('Topic already exist!')
    if find_topic_by_category(category):
        raise ValueError('Topic already exist in that category!')

    topic_data = Topics(id=topic_id, title=title, category=category)

    return create_topic(topic_data)
