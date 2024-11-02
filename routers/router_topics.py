from fastapi import APIRouter, Response, HTTPException, Header
from modules.replies import BestReply
from modules.topic import NewTopic
from services import topic_services, user_services


topics_router = APIRouter(prefix='/api/topics', tags=['Topics'])

# View Topics
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

# View Topic
@topics_router.get('/{topic_id}')
def get_topic_by_id(topic_id: int):
    try:
        return topic_services.find_topic_by_id(topic_id)
    except ValueError as e:
        return Response(status_code=400, content=str(e))

# ?
@topics_router.get('/category/{category_id}')
def get_topic_by_category(category_id: int):
    try:
        return topic_services.find_topic_by_category(category_id)
    except ValueError as e:
        return Response(status_code=400, content=str(e))

# Create Topic
@topics_router.post('/new_topic')
def create_new_topic(topic: NewTopic, token: str | None = Header()):
    # Check if user is authenticated
    user_data = user_services.authenticate(token)
    user_id = user_data["user_id"]
    locked_status = 1 if topic.is_locked else 0
    if not user_data:
        raise HTTPException(status_code=401, detail="Authorization token missing or invalid")
    try:
        return topic_services.create_topic(topic.title, topic.content, user_id, topic.category_id, locked_status)
    except ValueError as e:
        return Response(status_code=400, content=str(e))


# Choose Best Reply
@topics_router.post('/{topic_id}/replies{reply_id}')
def select_best_reply(reply: BestReply, token: str | None = Header()):
    # Check if user is authenticated
    user_data = user_services.authenticate(token)
    if not user_data:
        raise HTTPException(status_code=401, detail="Authorization token missing or invalid")

    try:
        return topic_services.choose_best_reply(reply.topic_id, reply.reply_id, user_data["user_id"])
    except ValueError as e:
        return Response(status_code=400, content=str(e))


@topics_router.delete('/{topic_id}')
def delete_topic(topic_id: int):
    try:
        return topic_services.remove_topic(topic_id)
    except ValueError as e:
        return Response(status_code=400, content=str(e))

# Lock Topic
@topics_router.post('/change_topic_lock_status')
def change_lock_status(topic_id: int, token: str | None = Header()):
    # Check if user is authenticated
    user_data = user_services.authenticate(token)
    if not user_data:
        raise HTTPException(status_code=401, detail="Authorization token missing or invalid")

    user_role = user_data["user_role"]
    if user_role == 1:
        raise HTTPException(status_code=403, detail="You do not have permission to grant access")

    try:
        return topic_services.change_topic_lock_status(topic_id)
    except ValueError as e:
        return Response(status_code=404, content=str(e))