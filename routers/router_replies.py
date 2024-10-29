from fastapi import APIRouter, HTTPException, Header
from starlette.responses import Response
from modules.replies import NewReply, GetReplyOnTopic, VoteRequest
from services.replies_services import vote_reply, create_reply, get_topics_with_best_replies, mark_best_reply
from services.user_services import authenticate, decode_jwt_token



replies_router = APIRouter(prefix='/replies')
votes_router = APIRouter(prefix='/votes', tags=['Replies'])
best_reply_router = APIRouter(prefix='/best_replies')

@replies_router.post('/create_reply')
def create_reply_route(reply: NewReply, authorization: str = Header(...)):
    user_info = authenticate(authorization)
    if not user_info:
        raise HTTPException(status_code=401, detail="Authorization token missing or invalid")

    try:
        return create_reply(reply.content, reply.topic_id, user_info["user_id"])
    except ValueError as e:
        return Response(status_code=400, content=str(e))


@votes_router.post('/reply/{reply_id}')
def post_vote_for_reply(reply_id: int, vote_request: VoteRequest, authorization: str = Header(...)):
    user_info = authenticate(authorization)
    try:
        return vote_reply(reply_id, vote_request.vote, user_info["user_id"])
    except ValueError as e:
        return Response(status_code=400, content=str(e))



@best_reply_router.post('/{topic_id}/replies/{reply_id}')
def choose_best_reply_route(topic_id: int, reply_id: int, authorization: str = Header(...)):
    user_info = authenticate(authorization)
    try:
        return mark_best_reply(topic_id, reply_id, user_info["user_id"])
    except ValueError as e:
        return HTTPException(status_code=400, detail=str(e))



# Choose Best Reply
@best_reply_router.get('/topics_with_best_replies')
def get_topics_with_best_replies_route(authorization: str = Header(...)):

    user_data = authenticate(authorization)
    if not user_data:
        raise HTTPException(status_code=401, detail="Authorization token missing or invalid")

    try:
        return get_topics_with_best_replies()
    except ValueError as e:
        return Response(status_code=400, content=str(e))
