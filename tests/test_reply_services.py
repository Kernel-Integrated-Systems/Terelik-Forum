import unittest
from unittest.mock import patch
from modules.replies import NewReply, VoteRequest
from services import replies_services as service

# Mock data for testing
mock_user = {
    "user_id": 1,
    "username": "alice"
}

mock_reply_data = {
    "reply_id": 1,
    "content": "This is a reply",
    "user_id": 1,
    "topic_id": 10,
    "created_at": "2023-10-31"
}

mock_topic_data = {
    "topic_id": 10,
    "title": "Sample Topic",
    "content": "Sample content",
    "user_id": 1,
    "category_id": 5,
    "best_reply_id": 1
}


class RepliesServiceTests(unittest.TestCase):

    def test_create_reply(self):
        with patch('services.replies_services.find_topic_by_id') as mock_find_topic, \
             patch('services.replies_services.insert_query') as mock_insert_query:

            mock_find_topic.return_value = mock_topic_data
            mock_insert_query.return_value = 1

            new_reply = NewReply(content="This is a reply", topic_id=10)
            result = service.create_reply(new_reply.content, new_reply.topic_id, mock_user["user_id"])

            self.assertEqual(result.content, "This is a reply")
            self.assertEqual(result.topic_id, 10)
            self.assertEqual(result.user_id, mock_user["user_id"])

    def test_vote_reply_upvote(self):
        with patch('services.replies_services.insert_query') as mock_insert_query:
            mock_insert_query.return_value = 1

            vote_request = VoteRequest(vote="upvote")
            result = service.vote_reply(1, vote_request.vote, mock_user["user_id"])

            self.assertIn("new vote added", result["message"])
            self.assertIn("reply 1", result["message"])

    def test_vote_reply_downvote(self):
        with patch('services.replies_services.insert_query') as mock_insert_query:
            mock_insert_query.return_value = 1

            vote_request = VoteRequest(vote="downvote")
            result = service.vote_reply(1, vote_request.vote, mock_user["user_id"])

            self.assertIn("new vote added", result["message"])
            self.assertIn("reply 1", result["message"])

    def test_mark_best_reply(self):
        with patch('services.replies_services.read_query') as mock_read_query, \
             patch('services.replies_services.update_query') as mock_update_query:

            mock_read_query.return_value = [mock_reply_data]
            mock_update_query.return_value = None

            result = service.mark_best_reply(topic_id=10, reply_id=1, user_id=mock_user["user_id"])

            self.assertIn("marked as the best reply", result["message"])
            self.assertIn("Reply ID 1", result["message"])

    def test_get_topics_with_best_replies(self):
        with patch('services.replies_services.read_query') as mock_read_query:
            mock_read_query.return_value = [(10, "Sample Topic", "Sample content", 1, 5, 1)]

            result = service.get_topics_with_best_replies()

            self.assertEqual(len(result), 1)
            self.assertEqual(result[0]["topic_id"], 10)
            self.assertEqual(result[0]["best_reply_id"], 1)

    def test_create_reply_with_invalid_topic(self):
        with patch('services.replies_services.find_topic_by_id') as mock_find_topic:
            mock_find_topic.side_effect = ValueError("Topic with ID 999 does not exist.")

            with self.assertRaises(ValueError) as context:
                service.create_reply("This is a reply", 999, mock_user["user_id"])

            self.assertEqual(str(context.exception), "Topic with ID 999 does not exist.")

    def test_vote_reply_with_invalid_vote_type(self):
        with self.assertRaises(ValueError) as context:
            service.vote_reply(1, "invalid_vote_type", mock_user["user_id"])

        self.assertEqual(str(context.exception), "The provided vote type invalid_vote_type is incorrect!")

    def test_mark_best_reply_with_invalid_reply(self):
        with patch('services.replies_services.read_query') as mock_read_query:
            mock_read_query.return_value = []

            with self.assertRaises(ValueError) as context:
                service.mark_best_reply(topic_id=10, reply_id=999, user_id=mock_user["user_id"])

            self.assertEqual(str(context.exception), "There is no valid reply with ID 999 for topic ID 10 and user ID 1!")
