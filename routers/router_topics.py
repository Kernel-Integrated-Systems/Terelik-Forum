from services.user_services import authenticate, decode_jwt_token
from fastapi import APIRouter, Response, HTTPException, Header
from modules.topic import NewTopic
from services.topic_services import (view_topics, create_topic, find_topic_by_id, find_topic_by_category, remove_topic)
from services.user_services import authenticate

topics_router = APIRouter(prefix='/topics', tags=['Topics'])


@topics_router.get('/')
def get_topics(authorization: str = Header(...)):
    user_info = authenticate(authorization)
    return view_topics()


@topics_router.get('/{topic_id}')
def get_topic_by_id(topic_id: int, authorization: str = Header(...)):
    user_info = authenticate(authorization)
    try:
        return find_topic_by_id(topic_id)
    except ValueError as e:
        return Response(status_code=400, content=str(e))


@topics_router.get('/category/{category_id}')
def get_topic_by_category(category_id: int, authorization: str = Header(...)):
    user_info = authenticate(authorization)
    try:
        return find_topic_by_category(category_id)
    except ValueError as e:
        return Response(status_code=400, content=str(e))


@topics_router.post('/new_topic')
def create_new_topic(topic: NewTopic, authorization: str = Header(...)):
    user_info = authenticate(authorization)
    if user_info["user_id"] != topic.user_id:
        raise HTTPException(status_code=403, detail="You cannot create topics on behalf of another user.")

    try:
        return create_topic(topic.title, topic.content, topic.user_id, topic.category_id)
    except ValueError as e:
        return Response(status_code=400, content=str(e))


@topics_router.delete('/{topic_id}')
def delete_topic(topic_id: int, authorization: str = Header(...)):
    user_info = authenticate(authorization)
    try:
        return remove_topic(topic_id)
    except ValueError as e:
        return Response(status_code=400, content=str(e))
