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
    new_vote = insert_query(queries.VOTE_ON_REPLY, (user_id, reply_id, vote_type))
    stamp = datetime.now()
    return VoteResponse(reply_id=reply_id, vote_type=vote_response, created_at=stamp)


def create_reply(content: str, topic_id: int, user_id: int):

    new_reply_id = insert_query(queries.NEW_REPLY, (content, user_id, topic_id))
    new_reply = Reply(reply_id=new_reply_id, content=content, user_id=user_id, topic_id=topic_id)

    return new_reply


# def vote_reply(reply_id: int, user_id: int, vote_type: str):
#     reply = find_reply_by_id(reply_id)
#     if not reply:
#         raise ValueError("Reply not found.")
#
#     existing_vote = next((v for v in votes if v.user_id == user_id and v.reply_id == reply_id), None)
#
#     if existing_vote:
#         if existing_vote.vote_type == vote_type:
#             return "Vote already recorded"
#         existing_vote.vote_type = vote_type
#     else:
#         new_vote = Vote(user_id=user_id, reply_id=reply_id, vote_type=vote_type)
#         votes.append(new_vote)
#
#     return f"Reply {vote_type}d successfully."


def get_all_topics_with_best_replies(topic_id: int, reply_id: int):
    user_id = 1
    best_reply = read_query(queries.CHOOSE_BEST_REPLY_ID, (user_id, topic_id, reply_id))
    if not best_reply:
        raise ValueError(f'There is no topic with ID {topic_id} for user ID {user_id}!')

    best_reply_id = best_reply[0][0]
    update_query(queries.ADD_BEST_REPLY_ON_TOPIC, (best_reply_id, reply_id))

    return {"message":f"Best reply ID {reply_id} is added to topic ID {topic_id}"}

