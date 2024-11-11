
from fastapi import APIRouter, HTTPException, Form, Request
from pydantic import BaseModel
from starlette.responses import RedirectResponse

from models.replies import VoteRequest
from services.replies_services import vote_reply, create_reply
from services.topic_services import check_topic_lock_status
from services.user_services import authenticate, decode_jwt_token

replies_router = APIRouter(prefix='/replies')
votes_router = APIRouter(prefix='/votes', tags=['Replies'])
best_reply_router = APIRouter(prefix='/best_replies')


@replies_router.post('/create_reply')
def create_reply_route(
        request: Request,
        topic_id: int = Form(...),
        content: str = Form(...)
):
    token = request.cookies.get("access_token")
    user_info = decode_jwt_token(token) if token else None
    if not user_info:
        raise HTTPException(status_code=401, detail="Unauthorized")

    if check_topic_lock_status(topic_id):
        raise HTTPException(status_code=403, detail="Topic is locked!")

    create_reply(content=content, topic_id=topic_id, user_id=user_info["user_id"])

    return RedirectResponse(url=f"/topics/{topic_id}", status_code=303)



@votes_router.post("/reply/{reply_id}")
def post_vote_for_reply(reply_id: int, request: Request, vote_data: VoteRequest):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Unauthorized")

    user_data = authenticate(request)
    if not user_data:
        raise HTTPException(status_code=401, detail="Unauthorized")

    result = vote_reply(reply_id=reply_id, vote_type=vote_data.vote_type, user_id=user_data["user_id"])
    return result
