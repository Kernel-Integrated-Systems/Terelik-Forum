from fastapi import APIRouter, HTTPException, Header
from starlette.responses import Response
from modules.replies import NewReply, Vote
from services import replies_services, user_services, topic_services


replies_router = APIRouter(prefix='/replies', tags=["Replies"])


# Create Reply
@replies_router.post('/reply')
def create_reply_route(reply: NewReply, token: str | None = Header()):
    # Check if user is authenticated
    user_data = user_services.authenticate(token)
    if not user_data:
        raise HTTPException(status_code=401, detail="Authorization token missing or invalid")

    is_locked = topic_services.check_topic_lock_status(reply.topic_id)
    if is_locked is None:
        raise HTTPException(status_code=404, detail="Topic does not exist!")
    if is_locked == 1:
         raise HTTPException(status_code=403, detail="Topic is locked!")
    try:
        return replies_services.create_reply(reply.content, reply.topic_id, user_data["user_id"])
    except ValueError as e:
        return Response(status_code=400, content=str(e))


# Upvote/Downvote a Reply
@replies_router.post('/{reply_id}')
def post_vote_for_reply(reply: Vote, token: str | None = Header()):
    # Check if user is authenticated
    user_data = user_services.authenticate(token)
    if not user_data:
        raise HTTPException(status_code=401, detail="Authorization token missing or invalid")

    is_locked = topic_services.check_topic_lock_status(reply.topic_id)
    if not is_locked:
        raise HTTPException(status_code=404, detail="Topic does not exist!")
    if is_locked == 1:
        raise HTTPException(status_code=403, detail="Topic is locked!")
    try:
        votes_list = replies_services.vote_reply(reply.reply_id, reply.vote)
        return votes_list
    except ValueError as e:
        return Response(status_code=400, content=str(e))

