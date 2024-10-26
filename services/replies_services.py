from modules.replies import Reply, Vote
from modules.topics import Topics
from percistance.connections import read_query, insert_query, update_query
from percistance.queries import VOTE_ON_REPLY, NEW_REPLY, CHOOSE_BEST_REPLY_ID, ADD_BEST_REPLY_ON_TOPIC
from services.topic_services import find_topic_by_id



def vote_reply(reply_id: int, vote_type: str, user_id: int):
    if vote_type.lower() == 'upvote':
        vote_type = 1
    elif vote_type.lower() == 'downvote':
        vote_type = 2
    else:
        raise ValueError(f'The provided vote type {vote_type} is incorrect!')

    new_vote = insert_query(VOTE_ON_REPLY, (user_id, reply_id, vote_type))
    return {"message": f"{new_vote} new vote added for reply {reply_id}."}


def create_reply(content: str, topic_id: int, user_id: int):
    find_topic_by_id(topic_id)
    new_reply_id = insert_query(NEW_REPLY, (content, user_id, topic_id))
    new_reply = Reply(reply_id=new_reply_id, content=content, user_id=user_id, topic_id=topic_id)
    return new_reply


def get_all_topics_with_best_replies(topic_id: int, reply_id: int, user_id: int):
    best_reply = read_query(CHOOSE_BEST_REPLY_ID, (user_id, topic_id, reply_id))
    if not best_reply:
        raise ValueError(f'There is no topic with ID {topic_id} for user ID {user_id}!')

    best_reply_id = best_reply[0][0]
    update_query(ADD_BEST_REPLY_ON_TOPIC, (best_reply_id, reply_id))
    return {"message": f"Best reply ID {reply_id} is added to topic ID {topic_id}"}