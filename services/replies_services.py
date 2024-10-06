from fastapi import HTTPException

from modules.replies import Reply, Vote
from percistance.data import replies, topics, votes
from services.topic_services import find_topic_by_id


def find_reply_by_id(reply_id):
    reply = next((r for r in replies if r.reply_id == reply_id), None)
    return reply


def create_reply(content: str, user_id: int, topic_id: int):
    topic = find_topic_by_id(topic_id)
    if not topic:
        raise ValueError('Topic not found')

    new_id = max(reply.reply_id for reply in replies) + 1 if replies else 1
    new_reply = Reply(reply_id=new_id, content=content, user_id=user_id, topic_id=topic_id)

    replies.append(new_reply)
    return new_reply


def vote_reply(reply_id: int, user_id: int, vote_type: str):
    reply = find_reply_by_id(reply_id)
    if not reply:
        raise ValueError("Reply not found.")

    existing_vote = next((v for v in votes if v.user_id == user_id and v.reply_id == reply_id), None)

    if existing_vote:
        if existing_vote.vote_type == vote_type:
            return "Vote already recorded"
        existing_vote.vote_type = vote_type
    else:
        new_vote = Vote(user_id=user_id, reply_id=reply_id, vote_type=vote_type)
        votes.append(new_vote)

    return f"Reply {vote_type}d successfully."




def choose_best_reply(topic_id: int, reply_id: int, user_id: int):
    topic = find_topic_by_id(topic_id)
    reply = find_reply_by_id(reply_id)

    if not topic:
        raise ValueError("Topic not found.")
    if topic.user_id != user_id:
        raise ValueError("Only the topic author can select the best reply.")
    if not reply:
        raise ValueError("Reply not found.")

    topic.best_reply_id = reply_id
    return "Best reply selected successfully."

def get_votes_for_reply(reply_id: int):
    reply_votes = [vote for vote in votes if vote.reply_id == reply_id]
    return reply_votes

def get_replies_for_topic(topic_id: int):
    topic_replies = [reply for reply in replies if reply.topic_id == topic_id]
    return topic_replies

