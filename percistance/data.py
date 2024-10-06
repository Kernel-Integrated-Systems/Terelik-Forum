from modules.messages import Message
from modules.users import User
from modules.topics import Topics
from modules.categories import Category
users = [
    User(id=1, username='John', email='john@terelikacademy.com', password='12345', role='admin', is_active=1),
    User(id=2, username='Maria', email='maria@terelikacademy.com', password='12345', role='user', is_active=1)
]

topics = [
    Topics(topic_id=1, title='New Topic', content='alabalaportokala', user_id=1, category_id=1),
    Topics(topic_id=2, title='Another Topic', content='babanana', user_id=2, category_id=2),
    Topics(topic_id=3, title='New Topic2', content='balabala', user_id=3, category_id=1)
]

categories = [
    Category(category_id=1, category_name="Category1"),
    Category(category_id=2, category_name="Category2"),
    Category(category_id=3, category_name="Category3")
]
messages = [
    Message(message_id=1, sender_id=2, receiver_id=1, content="Hello there! How are you?"),
    Message(message_id=2, sender_id=1, receiver_id=2, content="Hello, I'm fine, what about you?")
]
