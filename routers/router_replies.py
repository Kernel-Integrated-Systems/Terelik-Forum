from fastapi import APIRouter, HTTPException, Header
from starlette.responses import Response
from services.replies_services import vote_reply, create_reply, get_all_topics_with_best_replies
from services.user_services import authenticate, decode_jwt_token

replies_router = APIRouter(prefix='/replies', tags=['Replies'])
votes_router = APIRouter(prefix='/votes', tags=['Votes'])
best_reply_router = APIRouter(prefix='/best_replies', tags=['Best Replies'])


@replies_router.post('/create_reply')
def create_reply_route(reply_id: int, content: str, authorization: str = Header(...)):
    if not authenticate(authorization):
        raise HTTPException(status_code=401, detail="Authorization token missing or invalid")

    token_data = decode_jwt_token(authorization.split(" ")[1])
    try:
        return create_reply(content, reply_id, token_data["user_id"])
    except ValueError as e:
        return Response(status_code=400, content=str(e))


@votes_router.post('/reply/{reply_id}')
def post_vote_for_reply(reply_id: int, vote: str, authorization: str = Header(...)):
    if not authenticate(authorization):
        raise HTTPException(status_code=401, detail="Authorization token missing or invalid")

    token_data = decode_jwt_token(authorization.split(" ")[1])
    try:
        return vote_reply(reply_id, vote, token_data["user_id"])
    except ValueError as e:
        return Response(status_code=400, content=str(e))


@best_reply_router.post('/{topic_id}/replies/{reply_id}')
def choose_best_reply_route(topic_id: int, reply_id: int, authorization: str = Header(...)):
    if not authenticate(authorization):
        raise HTTPException(status_code=401, detail="Authorization token missing or invalid")

    token_data = decode_jwt_token(authorization.split(" ")[1])
    try:
        return get_all_topics_with_best_replies(topic_id, reply_id, token_data["user_id"])
    except ValueError as e:
        return Response(status_code=400, content=str(e))