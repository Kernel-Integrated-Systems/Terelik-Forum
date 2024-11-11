from datetime import datetime

from data.database import query_count
from models import replies
from models.replies import Reply
from percistance.connections import read_query, insert_query, update_query
from percistance.queries import VOTE_ON_REPLY, NEW_REPLY, CHOOSE_BEST_REPLY_ID, ADD_BEST_REPLY_ON_TOPIC
from services.topic_services import find_topic_by_id, check_topic_lock_status


from fastapi import APIRouter, HTTPException, Request
from services.user_services import authenticate
from percistance.connections import read_query, insert_query, update_query

votes_router = APIRouter(prefix='/votes', tags=['Replies'])

from fastapi import HTTPException

def vote_reply(reply_id: int, vote_type: str, user_id: int):
    vote_type_id = 1 if vote_type.lower() == 'upvote' else 2

    existing_vote = read_query("SELECT vote_id FROM Votes WHERE user_id = ? AND reply_id = ?", (user_id, reply_id))

    if existing_vote:
        update_query("UPDATE Votes SET vote_type = ? WHERE vote_id = ?", (vote_type_id, existing_vote[0][0]))
    else:
        insert_query("INSERT INTO Votes (user_id, reply_id, vote_type) VALUES (?, ?, ?)",
                     (user_id, reply_id, vote_type_id))

    upvote_count = query_count("SELECT COUNT(*) FROM Votes WHERE reply_id = ? AND vote_type = 1", (reply_id,))
    downvote_count = query_count("SELECT COUNT(*) FROM Votes WHERE reply_id = ? AND vote_type = 2", (reply_id,))

    return {"upvotes": upvote_count, "downvotes": downvote_count}


from datetime import datetime
from typing import List, Dict


class ReplyWithVotes:
    def __init__(self, reply_id: int, content: str, user_id: int, topic_id: int, created_at: datetime, upvotes: int,
                 downvotes: int):
        self.reply_id = reply_id
        self.content = content
        self.user_id = user_id
        self.topic_id = topic_id
        self.created_at = created_at
        self.upvotes = upvotes
        self.downvotes = downvotes


def get_replies_with_vote_counts(topic_id: int) -> List[ReplyWithVotes]:
    replies_data = read_query("SELECT reply_id, content, user_id, topic_id, created_at FROM replies WHERE topic_id = ?",
                              (topic_id,))
    replies_with_votes = []

    for reply in replies_data:
        reply_id = reply[0]
        upvote_count = query_count("SELECT COUNT(*) FROM Votes WHERE reply_id = ? AND vote_type = 1", (reply_id,))
        downvote_count = query_count("SELECT COUNT(*) FROM Votes WHERE reply_id = ? AND vote_type = 2", (reply_id,))

        replies_with_votes.append(
            ReplyWithVotes(
                reply_id=reply_id,
                content=reply[1],
                user_id=reply[2],
                topic_id=reply[3],
                created_at=reply[4],
                upvotes=upvote_count,
                downvotes=downvote_count
            )
        )

    return replies_with_votes


def get_replies_for_topic(topic_id: int):
    topic_replies = [reply for reply in replies if reply.topic_id == topic_id]
    return topic_replies


def create_reply(content: str, topic_id: int, user_id: int):
    find_topic_by_id(topic_id)

    new_reply_id = insert_query(NEW_REPLY, (content, user_id, topic_id))
    new_reply = Reply(reply_id=new_reply_id, content=content, user_id=user_id, topic_id=topic_id,
                      created_at=datetime.now())

    return new_reply


def get_all_topics_with_best_replies(topic_id: int, reply_id: int):
    user_id = 1
    best_reply = read_query(CHOOSE_BEST_REPLY_ID, (user_id, topic_id, reply_id))
    if not best_reply:
        raise ValueError(f'There is no topic with ID {topic_id} for user ID {user_id}!')

    best_reply_id = best_reply[0][0]
    update_query(ADD_BEST_REPLY_ON_TOPIC, (best_reply_id, reply_id))
    return {"message": f"Best reply ID {reply_id} is added to topic ID {topic_id}"}

