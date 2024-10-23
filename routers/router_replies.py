from fastapi import APIRouter, HTTPException
from starlette.responses import Response

from modules.replies import NewReply
from services.replies_services import vote_reply, create_reply, get_all_topics_with_best_replies
from services.user_services import authenticate

replies_router = APIRouter(prefix='/replies')
votes_router = APIRouter(prefix='/votes', tags=['Replies'])
best_reply_router = APIRouter(prefix='/best_replies')


# Create Reply
@replies_router.post('/create_reply')
def create_reply_route(reply: NewReply, token: str | None = None):
    if not authenticate(token):
        raise HTTPException(status_code=401, detail="Authorization token missing or invalid")

    try:
        return create_reply(reply.content, reply.reply_id)
    except ValueError as e:
        return Response(status_code=400, content=str(e))


# @votes_router.post('/reply/{reply_id}')
# def vote_reply_route(reply_id: int, vote: Vote):
#     try:
#         result = vote_reply(reply_id, vote.user_id, vote.vote_type)
#         return result
#     except ValueError as e:
#         return Response(status_code=400, content=str(e))


# @best_reply_router.patch('/{topic_id}/best_reply/{reply_id}')
# def choose_best_reply_route(topic_id: int, reply_id: int, user_id: int):
#     topic = find_topic_by_id(topic_id)
#     reply = find_reply_by_id(reply_id)
#
#     if not topic:
#         raise HTTPException(status_code=404, detail="Topic not found.")
#
#     if topic.user_id != user_id:
#         raise HTTPException(status_code=403, detail="Only the topic author can select the best reply.")
#
#     if not reply:
#         raise HTTPException(status_code=404, detail="Reply not found.")
#     try:
#         topic.best_reply_id = reply_id
#     except ValueError as err:
#         raise HTTPException(status_code=404, detail=str(err))
#     return {"detail": "Best reply selected successfully."}
#

# Upvote/Downvote a Reply
@votes_router.post('/reply/{reply_id}')
def post_vote_for_reply(reply_id: int, vote: str, token: str | None = None):
    if not authenticate(token):
        raise HTTPException(status_code=401, detail="Authorization token missing or invalid")

    try:
        votes_list = vote_reply(reply_id, vote)
        return votes_list
    except ValueError as e:
        return Response(status_code=400, content=str(e))


# @best_reply_router.get('/{topic_id}')
# def get_best_reply_route(topic_id: int):
#     try:
#         best_reply = get_best_reply_for_topic(topic_id)
#         if not best_reply:
#             return {"detail": "No best reply selected for this topic."}
#         return best_reply
#     except ValueError as err:
#         raise HTTPException(status_code=404, detail=str(err))
#
#

# Choose Best Reply
@best_reply_router.get('/{topic_id}/replies{reply_id}')
def get_all_topics_with_best_replies_route(topic_id: int, reply_id: int, token: str | None = None):
    if not authenticate(token):
        raise HTTPException(status_code=401, detail="Authorization token missing or invalid")

    try:
        return get_all_topics_with_best_replies(topic_id, reply_id)
    except ValueError as e:
        return Response(status_code=400, content=str(e))