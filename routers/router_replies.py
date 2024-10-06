from fastapi import APIRouter, HTTPException

from modules.replies import Reply, Vote
from services.replies_services import create_reply, vote_reply, choose_best_reply, get_replies_for_topic, \
    get_votes_for_reply

replies_router = APIRouter(prefix='/replies')

@replies_router.post('/create_reply')  #tested
def create_reply_route(reply: Reply):
    try:
        reply_obj = create_reply(reply.content, reply.user_id, reply.topic_id)
        return reply_obj
    except ValueError as err:
        raise HTTPException(status_code=400, detail=str(err))



votes_router = APIRouter(prefix='/votes')


@votes_router.post('/reply/{reply_id}')
def vote_reply_route(reply_id: int, vote: Vote):
    if vote.vote_type not in ['upvote', 'downvote']:
        raise HTTPException(status_code=400, detail="Invalid vote type.")

    try:
        result = vote_reply(reply_id, vote.user_id, vote.vote_type)
        return result
    except ValueError as err:
        raise HTTPException(status_code=404, detail=str(err))


best_reply_router = APIRouter(prefix='/topics')

@best_reply_router.patch('/{topic_id}/best_reply/{reply_id}')
def choose_best_reply_route(topic_id: int, reply_id: int, user_id: int):
    try:
        result = choose_best_reply(topic_id, reply_id, user_id)
        return result
    except ValueError as err:
        raise HTTPException(status_code=400, detail=str(err))


@replies_router.get('/topic/{topic_id}')
def get_replies_by_topic(topic_id: int):
    try:
        replies_list = get_replies_for_topic(topic_id)
        return replies_list
    except Exception as err:
        raise HTTPException(status_code=400, detail=str(err))

@votes_router.get('/reply/{reply_id}')
def get_votes_by_reply(reply_id: int):
    try:
        votes_list = get_votes_for_reply(reply_id)
        return votes_list
    except Exception as err:
        raise HTTPException(status_code=400, detail=str(err))