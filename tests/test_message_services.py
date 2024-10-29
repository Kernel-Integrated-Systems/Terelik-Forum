import unittest
from unittest.mock import Mock, patch
from modules.messages import NewMessage, NewMessageRespond
from services import message_services as service

mock_message_service = Mock(spec='services.message_services')

service.message_services = mock_message_service


# Mock Data
mock_user_sender = {
    "id": 1,
    "username": "alice"
}

mock_user_receiver = {
    "id": 2,
    "username": "bob"
}

mock_message_data = [
    ("alice", "bob", "Hello Bob!"),
    ("bob", "alice", "Hi Alice!")
]

def create_message():
    return NewMessageRespond(
        sender=mock_user_sender["username"],
        receiver=mock_user_receiver["username"],
        content=mock_message_data[1][2]
    )


def create_new_message_respond(sender="alice", receiver="bob", content="Hello!"):
    return NewMessageRespond(sender=sender, receiver=receiver, content=content)


class MessageService_Should(unittest.TestCase):

    def test_get_messages(self):
        with patch('services.message_services.read_query') as mock_get:
            mock_get.return_value = mock_message_data

            result = list(service.get_messages(1))  # Call your service function
            expected = [
                create_new_message_respond("alice", "bob", "Hello Bob!"),
                create_new_message_respond("bob", "alice", "Hi Alice!")
            ]

            self.assertEqual(result, expected)


    def test_get_message_by_id(self):
        with patch('services.message_services.read_query') as mock_get:
            mock_get.return_value = [
                ("alice", "bob", "Hello Bob!")  # Simulating a single message
            ]

            result = list(service.get_message_by_id(current_user_id=1, target_user_id=2))
            expected = [
                NewMessageRespond(sender="alice", receiver="bob", content="Hello Bob!")
            ]

            self.assertEqual(result, expected)


    def test_create_message(self):
        with (patch('services.message_services.insert_query') as mock_insert_query):

            mock_insert_query.side_effect = [
                [mock_user_sender],
                [mock_user_receiver]
            ]

            mock_insert_query.return_value = 1

            new_message = NewMessage(sender_id=1, receiver_id=2, content="Hello Bob!")
            result = service.create_message(new_message)
            result_obj = NewMessageRespond(**result)
            expected = NewMessageRespond(sender="alice", receiver="bob", content="Hello Bob!")

            self.assertEqual(result_obj, expected)


