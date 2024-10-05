from modules.messages import Message
from modules.users import User


users = [
    User(id=1, username='John', email='john@terelikacademy.com', password='12345', role='admin', is_active=1),
    User(id=2, username='Maria', email='maria@terelikacademy.com', password='12345', role='user', is_active=1)
]

messages = [
    Message(message_id=1, sender_id=2, receiver_id=1, content="Hello there! How are you?"),
    Message(message_id=2, sender_id=1, receiver_id=2, content="Hello, I'm fine, what about you?")
]
