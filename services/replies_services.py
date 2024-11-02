from datetime import datetime
from modules.replies import Reply, VoteResponse
from percistance.connections import read_query, insert_query, update_query
from percistance import queries


def vote_reply(reply_id: int, vote_type: int, user_id: int):
    vote_response = ''
    if vote_type == 1:
        vote_response = 'upvote'
    elif vote_type == 2:
        vote_response = 'downvote'
    else:
        raise ValueError(f'The provided vote type {vote_type} is incorrect!')
    vote_exists = read_query(queries.CHECK_VOTE_EXISTS, (user_id, reply_id, vote_type))
    if vote_exists[0][0] > 0:
        raise ValueError('You have already voted for this reply')
    insert_query(queries.VOTE_ON_REPLY, (user_id, reply_id, vote_type))
    stamp = datetime.now()
    return VoteResponse(reply_id=reply_id, vote_type=vote_response, created_at=stamp)


def create_reply(content: str, topic_id: int, user_id: int):

    new_reply_id = insert_query(queries.NEW_REPLY, (content, user_id, topic_id))
    new_reply = Reply(reply_id=new_reply_id, content=content, user_id=user_id, topic_id=topic_id)

    return new_reply


def get_all_topics_with_best_replies(topic_id: int, reply_id: int):
    user_id = 1
    best_reply = read_query(queries.CHOOSE_BEST_REPLY_ID, (user_id, topic_id, reply_id))
    if not best_reply:
        raise ValueError(f'There is no topic with ID {topic_id} for user ID {user_id}!')

    best_reply_id = best_reply[0][0]
    update_query(queries.ADD_BEST_REPLY_ON_TOPIC, (best_reply_id, reply_id))

    return {"message":f"Best reply ID {reply_id} is added to topic ID {topic_id}"}

