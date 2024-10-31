from modules.replies import BestReply
from services import topic_services
from services.user_services import authenticate, decode_jwt_token
from fastapi import APIRouter, Response, HTTPException, Header
from modules.topic import NewTopic
import services.topic_services
from services.user_services import authenticate

topics_router = APIRouter(prefix='/topics', tags=['Topics'])


@topics_router.get('/')
def get_topics(
        sort: str | None = None,
        sort_by: str | None = None,
        search: str | None = None,
        page: int = 1,
        page_size: int = 4):
    found_topics = topic_services.view_topics(search, page, page_size)

    if sort and (sort == 'asc' or sort == 'desc'):
        return topic_services.sort_topics(found_topics, reverse=sort == 'desc', attribute=sort_by)
    return found_topics


@topics_router.get('/{topic_id}')
def get_topic_by_id(topic_id: int):
    try:
        return topic_services.find_topic_by_id(topic_id)
    except ValueError as e:
        return Response(status_code=400, content=str(e))


@topics_router.get('/category/{category_id}')
def get_topic_by_category(category_id: int):
    try:
        return topic_services.find_topic_by_category(category_id)
    except ValueError as e:
        return Response(status_code=400, content=str(e))


@topics_router.post('/new_topic')
def create_new_topic(topic: NewTopic, authorization: str = Header(...)):
    user_info = authenticate(authorization)
    if user_info["user_id"] != topic.user_id:
        raise HTTPException(status_code=403, detail="You cannot create topics on behalf of another user.")

    try:
        return topic_services.create_topic(topic.title, topic.content, topic.user_id, topic.category_id)
    except ValueError as e:
        return Response(status_code=400, content=str(e))

# Choose Best Reply
@topics_router.post('/{topic_id}/replies{reply_id}')
def select_best_reply(reply: BestReply, authorization: str = Header(...)):
    # Check if user is authenticated
    user_data = authenticate(authorization)
    if not user_data:
        raise HTTPException(status_code=401, detail="Authorization token missing or invalid")

    try:
        return topic_services.choose_best_reply(reply.topic_id, reply.reply_id, user_data["user_id"])
    except ValueError as e:
        return Response(status_code=400, content=str(e))

@topics_router.delete('/{topic_id}')
def delete_topic(topic_id: int, authorization: str = Header(...)):
    user_info = authenticate(authorization)

    if user_info["user_role"] == 1:
        raise HTTPException(status_code=403, detail="You do not have permission to grant access")

    try:
        return topic_services.remove_topic(topic_id)
    except ValueError as e:
        return Response(status_code=400, content=str(e))

@topics_router.post('/change_topic_lock_status')
def change_lock_status(topic_id: int, authorization: str = Header(...)):
    user_data = authenticate(authorization)
    user_role = user_data["user_role"]
    if user_role == 1:
        raise HTTPException(status_code=403, detail="You do not have permission to grant access")

    try:
        return topic_services.change_topic_lock_status(topic_id)
    except ValueError as e:
        return Response(status_code=404, content=str(e))