from datetime import datetime

from modules.replies import Reply, Vote, VoteResponse
from percistance.connections import read_query, insert_query, update_query
from percistance.queries import VOTE_ON_REPLY, NEW_REPLY, CHOOSE_BEST_REPLY_ID, ADD_BEST_REPLY_ON_TOPIC, \
    GET_TOPICS_WITH_BEST_REPLY
from services.topic_services import find_topic_by_id


def vote_reply(reply_id: int, vote_type: int, user_id: int):
    vote_response = ''
    if vote_type == 1:
        vote_response = 'upvote'
    elif vote_type == 2:
        vote_response = 'downvote'
    else:
        raise ValueError(f'The provided vote type {vote_type} is incorrect!')
    new_vote = insert_query(VOTE_ON_REPLY, (user_id, reply_id, vote_type))
    stamp = datetime.now()
    return VoteResponse(reply_id=reply_id, vote_type=vote_response, created_at=stamp)

def create_reply(content: str, topic_id: int, user_id: int):
    new_reply_id = insert_query(NEW_REPLY, (content, user_id, topic_id))
    new_reply = Reply(reply_id=new_reply_id, content=content, user_id=user_id, topic_id=topic_id)

    return new_reply

