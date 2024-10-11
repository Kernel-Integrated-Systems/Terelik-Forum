from modules import topics
from percistance import data



def view_topics():
    sql = '''SELECT topic_id, title, content, user_id, category_id FROM topics'''
    return (topics.Topics.view_topics(*row) for row in data.read_query(sql))
