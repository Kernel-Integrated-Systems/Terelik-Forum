
from datetime import datetime
from modules.topics import Topics
from modules.messages import Message
from modules.users import User
from modules.replies import Reply, Vote


users = [
    User(id=1, username='John', email='john@terelikacademy.com', password='12345', role='admin', is_active=1),
    User(id=2, username='Maria', email='maria@terelikacademy.com', password='12345', role='user', is_active=1)
]


topics = [
    Topics(topic_id=1, title='New Topic', content='alabalaportokala', user_id=1, category_id=1),
    Topics(topic_id=2, title='Another Topic', content='babanana', user_id=2, category_id=2),
    Topics(topic_id=3, title='New Topic2', content='balabala', user_id=3, category_id=1)
]



replies = [
    Reply(reply_id=1, content='I prefer Python for backend, easier to write.', user_id=2, topic_id=1),
    Reply(reply_id=2, content='Java has better performance for large-scale systems.', user_id=3, topic_id=1),
    Reply(reply_id=3, content='React is more flexible, Angular is too opinionated.', user_id=4, topic_id=2),
    Reply(reply_id=4, content='REST APIs should be stateless and use proper HTTP methods.', user_id=5, topic_id=3),
    Reply(reply_id=5, content='Flask is simpler for small projects.', user_id=6, topic_id=4),
    Reply(reply_id=6, content='Django is more robust with built-in features.', user_id=7, topic_id=4),
    Reply(reply_id=7, content='WebSockets are great for real-time communication, especially for chats.', user_id=8, topic_id=5)
]

votes = [
    Vote(vote_id=1, user_id=2, reply_id=1, vote_type='upvote', created_at=datetime(2024, 10, 1, 12, 0)),
    Vote(vote_id=2, user_id=3, reply_id=1, vote_type='downvote', created_at=datetime(2024, 10, 1, 12, 5)),
    Vote(vote_id=3, user_id=4, reply_id=2, vote_type='upvote', created_at=datetime(2024, 10, 1, 12, 10)),
    Vote(vote_id=4, user_id=5, reply_id=2, vote_type='upvote', created_at=datetime(2024, 10, 1, 12, 15)),
    Vote(vote_id=5, user_id=6, reply_id=3, vote_type='downvote', created_at=datetime(2024, 10, 1, 12, 20)),
    Vote(vote_id=6, user_id=7, reply_id=4, vote_type='upvote', created_at=datetime(2024, 10, 1, 12, 25)),
    Vote(vote_id=7, user_id=8, reply_id=5, vote_type='upvote', created_at=datetime(2024, 10, 1, 12, 30)),
    Vote(vote_id=8, user_id=2, reply_id=6, vote_type='downvote', created_at=datetime(2024, 10, 1, 12, 35)),
    Vote(vote_id=9, user_id=3, reply_id=7, vote_type='upvote', created_at=datetime(2024, 10, 1, 12, 40)),
    Vote(vote_id=10, user_id=4, reply_id=7, vote_type='upvote', created_at=datetime(2024, 10, 1, 12, 45)),

messages = [
    Message(message_id=1, sender_id=2, receiver_id=1, content="Hello there! How are you?"),
    Message(message_id=2, sender_id=1, receiver_id=2, content="Hello, I'm fine, what about you?")
]
