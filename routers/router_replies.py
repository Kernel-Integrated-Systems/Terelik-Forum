from fastapi import APIRouter, HTTPException, Header
from starlette.responses import Response
from modules.replies import NewReply, GetReplyOnTopic, Vote
from services import replies_services, user_services, topic_services


replies_router = APIRouter(prefix='/replies', tags=["Replies"])
# votes_router = APIRouter(prefix='/votes', tags=['Replies'])
# best_reply_router = APIRouter(prefix='/best_replies')


# Create Reply
@replies_router.post('/reply')
def create_reply_route(reply: NewReply, token: str | None = Header()):
    # Check if user is authenticated
    user_data = user_services.authenticate(token)
    if not user_data:
        raise HTTPException(status_code=401, detail="Authorization token missing or invalid")

    is_locked = topic_services.check_topic_lock_status(reply.topic_id)

    if is_locked == 1:
         raise HTTPException(status_code=403, detail="Category is locked!")
    try:
        return replies_services.create_reply(reply.content, reply.topic_id, user_data["user_id"])
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
@replies_router.post('/{reply_id}')
def post_vote_for_reply(reply: Vote, token: str | None = Header()):
    # Check if user is authenticated
    user_data = user_services.authenticate(token)
    if not user_data:
        raise HTTPException(status_code=401, detail="Authorization token missing or invalid")

    try:
        votes_list = replies_services.vote_reply(reply.reply_id, reply.vote)
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
@replies_router.get('/{topic_id}/replies{reply_id}')
def get_all_topics_with_best_replies_route(reply: GetReplyOnTopic, token: str | None = Header()):
    # Check if user is authenticated
    user_data = user_services.authenticate(token)
    if not user_data:
        raise HTTPException(status_code=401, detail="Authorization token missing or invalid")

    try:
        return replies_services.get_all_topics_with_best_replies(reply.topic_id, reply.reply_id)
    except ValueError as e:
        return Response(status_code=400, content=str(e))