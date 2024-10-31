import unittest
from unittest.mock import patch
from modules.messages import NewMessage, NewMessageRespond
from services import messages_services as service

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


def create_new_message_respond(sender="alice", receiver="bob", content="Hello!"):
    return NewMessageRespond(sender=sender, receiver=receiver, content=content)


class MessageService_Should(unittest.TestCase):

    @patch('services.message_services.read_query')  # Correctly patch here
    def test_get_messages(self, mock_read_query):
        # Mock return value to simulate fetching messages
        mock_read_query.return_value = mock_message_data

        result = list(service.get_messages(1))  # Call your service function
        expected = [
            create_new_message_respond("alice", "bob", "Hello Bob!"),
            create_new_message_respond("bob", "alice", "Hi Alice!")
        ]

        self.assertEqual(result, expected)


    @patch('services.message_services.read_query')
    def test_get_message_by_id(self, mock_read_query):
        # Mock return value to simulate fetching a message by ID
        mock_read_query.return_value = [
            ("alice", "bob", "Hello Bob!")  # Simulating a single message
        ]

        result = list(service.get_message_by_id(current_user_id=1, target_user_id=2))
        expected = [
            NewMessageRespond(sender="alice", receiver="bob", content="Hello Bob!")
        ]

        self.assertEqual(result, expected)


    # @patch('percistance.connections.insert_query')
    # @patch('services.user_services.get_user_by_id')
    # def test_create_message(self, mock_get_user_by_id, mock_insert_query):
    #
    #     mock_get_user_by_id.side_effect = [mock_user_sender, mock_user_receiver]
    #     mock_insert_query.return_value = 1
    #     new_message = NewMessage(sender_id=1, receiver_id=2, content="Hello Bob!")
    #     result = service.create_message(new_message)
    #
    #     expected = service.create_message("alice", "bob", "Hello Bob!")
    #     self.assertEqual(result, expected)


# if __name__ == "__main__":
#     unittest.main()
