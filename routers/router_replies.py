from fastapi import APIRouter, HTTPException, Header
from starlette.responses import Response
from modules.replies import NewReply, Vote
from services.replies_services import vote_reply, create_reply
from services.topic_services import check_topic_lock_status
from services.user_services import authenticate, decode_jwt_token



replies_router = APIRouter(prefix='/replies')
votes_router = APIRouter(prefix='/votes', tags=['Replies'])
best_reply_router = APIRouter(prefix='/best_replies')

@replies_router.post('/create_reply')
def create_reply_route(reply: NewReply, authorization: str = Header(...)):
    user_info = authenticate(authorization)
    is_locked = check_topic_lock_status(reply.topic_id)
    if is_locked is None:
        raise HTTPException(status_code=404, detail="Topic does not exist!")
    if is_locked == 1:
        raise HTTPException(status_code=403, detail="Topic is locked!")
    try:
        return create_reply(reply.content, reply.topic_id, user_info["user_id"])
    except ValueError as e:
        return Response(status_code=400, content=str(e))

@votes_router.post('/reply/{reply_id}')
def post_vote_for_reply(reply: Vote, authorization: str = Header(...)):
    # Check if user is authenticated
    user_data = authenticate(authorization)
    if not user_data:
        raise HTTPException(status_code=401, detail="Authorization token missing or invalid")

    is_locked = check_topic_lock_status(reply.reply_id)
    if is_locked is None:
        raise HTTPException(status_code=404, detail="Topic does not exist!")
    if is_locked == 1:
        raise HTTPException(status_code=403, detail="Topic is locked!")
    try:
        votes_list = vote_reply(reply.reply_id, reply.vote_type, user_data["user_id"])
        return votes_list
    except ValueError as e:
        return Response(status_code=400, content=str(e))


