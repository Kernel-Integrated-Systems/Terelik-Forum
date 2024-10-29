from fastapi import APIRouter, Response, HTTPException, Header
from modules.topic import NewTopic
from services.topic_services import (view_topics, create_topic, find_topic_by_id, find_topic_by_category, remove_topic,
                                     change_topic_lock_status)
from services.user_services import authenticate

topics_router = APIRouter(prefix='/topics', tags=['Topics'])


@topics_router.get('/')
def get_topics():
    return view_topics()


@topics_router.get('/{topic_id}')
def get_topic_by_id(topic_id: int):
    try:
        return find_topic_by_id(topic_id)
    except ValueError as e:
        return Response(status_code=400, content=str(e))


@topics_router.get('/category/{category_id}')
def get_topic_by_category(category_id: int):
    try:
        return find_topic_by_category(category_id)
    except ValueError as e:
        return Response(status_code=400, content=str(e))


@topics_router.post('/new_topic')
def create_new_topic(topic: NewTopic, token: str | None = Header()):
    # Check if user is authenticated
    user_data = authenticate(token)
    if not user_data:
        raise HTTPException(status_code=401, detail="Authorization token missing or invalid")
    try:
        return create_topic(topic.title, topic.content, topic.user_id, topic.category_id)
    except ValueError as e:
        return Response(status_code=400, content=str(e))


@topics_router.delete('/{topic_id}')
def delete_topic(topic_id: int):
    try:
        return remove_topic(topic_id)
    except ValueError as e:
        return Response(status_code=400, content=str(e))


@topics_router.post('/change_topic_lock_status')
def change_lock_status(topic_id: int, token: str | None = Header()):
    # Check if user is authenticated
    user_data = authenticate(token)
    if not user_data:
        raise HTTPException(status_code=401, detail="Authorization token missing or invalid")

    user_role = user_data["user_role"]
    if user_role == 1:
        raise HTTPException(status_code=403, detail="You do not have permission to grant access")

    try:
        return change_topic_lock_status(topic_id)
    except ValueError as e:
        return Response(status_code=404, content=str(e))