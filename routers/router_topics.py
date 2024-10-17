from fastapi import APIRouter, Response

from percistance.data import authenticate
from services.topic_services import (view_topics, create_topic, find_topic_by_id, find_topic_by_category, remove_topic)


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
def create_new_topic(title: str, content: str, user_id: int, category_id: int, token: str | None = None):
    auth = authenticate(token)
    if not auth:
        return Response(status_code=404, content=str('Unauthorized access!'))
    try:
        return create_topic(title, content, user_id, category_id)
    except ValueError as e:
        return Response(status_code=400, content=str(e))


@topics_router.delete('/{topic_id}')
def delete_topic(topic_id: int, token: str | None = None):
    authenticate(token)
    try:
        return remove_topic(topic_id)
    except ValueError as e:
        return Response(status_code=400, content=str(e))
