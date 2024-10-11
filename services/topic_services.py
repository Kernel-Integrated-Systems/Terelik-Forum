
from modules import topics
from percistance import data



def view_topics():
    sql = '''SELECT topic_id, title, content, user_id, category_id FROM topics'''
    return (topics.Topics.view_topics(*row) for row in data.read_query(sql))


def create_topic(title: str, content: str, user_id: int, category: int):
    new_id = max(topic.topic_id for topic in topics) + 1 if topics else 1
    new_topic = Topics(topic_id=new_id, title=title, content=content, user_id=user_id, category_id=category)
    topics.append(new_topic)
    return new_topic


def find_topic_by_id(id: int):
    for topic in topics:
        if topic.topic_id == id:
            return topic

def find_topic_by_title(title: str):
    for topic in topics:
        if title.lower() in topic.title.lower():
            return topic


def find_topic_by_category(category_id: int):
    topic_l = [t for t in topics if t.category_id == category_id]
    return topic_l
