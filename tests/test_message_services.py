import unittest
from unittest.mock import patch
from modules.messages import NewMessage, NewMessageRespond
from services import message_services as service

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


    @patch('percistance.connections.insert_query')
    @patch('services.user_services.get_user_by_id')
    def test_create_message(self, mock_get_user_by_id, mock_insert_query):

        mock_get_user_by_id.side_effect = [mock_user_sender, mock_user_receiver]
        mock_insert_query.return_value = 1
        new_message = NewMessage(sender_id=1, receiver_id=2, content="Hello Bob!")
        result = service.create_message(new_message)

        expected = create_new_message_respond("alice", "bob", "Hello Bob!")
        self.assertEqual(result, expected)

    @patch('services.user_services.get_user_by_id')
    @patch('services.message_services.create_message')
    def test_post_new_message(self, mock_create_message, mock_get_user_by_id):
        # Mock return values for users
        mock_get_user_by_id.side_effect = [mock_user_sender, mock_user_receiver]

        # Mock the create_message function to simulate successful message creation
        mock_create_message.return_value = create_new_message_respond("alice", "bob", "Hello Bob!")

        result = service.post_new_message(sender=1, receiver=2, text="Hello Bob!")
        expected = create_new_message_respond("alice", "bob", "Hello Bob!")

        self.assertEqual(result, expected)

    @patch('services.user_services.get_user_by_id')
    def test_post_new_message_invalid_sender(self, mock_get_user_by_id):
        # Simulate a non-existent sender
        mock_get_user_by_id.return_value = None

        with self.assertRaises(ValueError) as context:
            service.post_new_message(sender=99, receiver=2, text="Hello Bob!")

        self.assertEqual(str(context.exception), "Sender with ID 99 does not exist!")

    @patch('services.user_services.get_user_by_id')
    def test_post_new_message_invalid_receiver(self, mock_get_user_by_id):
        # Simulate a non-existent receiver
        mock_get_user_by_id.side_effect = [mock_user_sender, None]

        with self.assertRaises(ValueError) as context:
            service.post_new_message(sender=1, receiver=99, text="Hello Bob!")

        self.assertEqual(str(context.exception), "Receiver with ID 99 does not exist!")

    def test_post_new_message_empty_content(self):
        with self.assertRaises(ValueError) as context:
            service.post_new_message(sender=1, receiver=2, text="")

        self.assertEqual(str(context.exception), "Message content cannot be empty!")


if __name__ == "__main__":
    unittest.main()
