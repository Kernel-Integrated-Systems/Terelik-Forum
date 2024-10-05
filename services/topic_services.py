from modules.topics import Topics
from percistance.data import topics


def create_topic(title: str, category: str):
    new_id = max(topic.topic_id for topic in topics) + 1 if topics else 1
    new_topic = Topics(topic_id=new_id, title=title, category=category)
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
        if title.lower() in topic.title.lower():
            return topic


def find_topic_by_category(category: str):
    for topic in topics:
        if topic.category.lower() == category.lower():
            return topic
    return None
