from modules.users import User
from modules.topics import Topics

users = [
    User(id=1, username='John', email='john@terelikacademy.com', password='12345', role='admin', is_active=1),
    User(id=2, username='Maria', email='maria@terelikacademy.com', password='12345', role='user', is_active=1)
]

topics = [
    Topics(topic_id=1, title='New Topic', category='1st Category'),
    Topics(topic_id=2, title='Another Topic', category='2st Category')
]
