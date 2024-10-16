from fastapi import APIRouter, HTTPException
from starlette.responses import Response

from modules.replies import Reply, Vote
from services.replies_services import vote_reply
from services.topic_services import find_topic_by_id

replies_router = APIRouter(prefix='/replies')
votes_router = APIRouter(prefix='/votes')
best_reply_router = APIRouter(prefix='/best_replies')


# @replies_router.post('/create_reply')
# def create_reply_route(reply: Reply):
#     try:
#         reply_obj = create_reply(reply.content, reply.user_id, reply.topic_id)
#         return reply_obj
#     except ValueError as err:
#         raise HTTPException(status_code=400, detail=str(err))


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
#
# @replies_router.get('/topic/{topic_id}')
# def get_replies_by_topic(topic_id: int):
#     try:
#         replies_list = get_replies_for_topic(topic_id)
#         return replies_list
#     except Exception as err:
#         raise HTTPException(status_code=400, detail=str(err))


@votes_router.post('/reply/{reply_id}')
def post_vote_for_reply(reply_id: int, vote: str):
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
# @best_reply_router.get('/')
# def get_all_topics_with_best_replies_route():
#     try:
#         topics_with_best_replies = get_all_topics_with_best_replies()
#         return topics_with_best_replies
#     except Exception as err:
#         raise HTTPException(status_code=500, detail=str(err))