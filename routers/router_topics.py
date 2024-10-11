from fastapi import APIRouter, HTTPException, Response

from services import topic_services
from services.topic_services import (view_topics, create_topic, find_topic_by_id, find_topic_by_category)
from percistance.data import topics

topics_router = APIRouter(prefix='/topics')


@topics_router.get('/')
def get_topics():



@topics_router.get('/{topic_id}')
def get_topic_by_id(topic_id: int):
    topic = find_topic_by_id(topic_id)
    if not topic:
        raise HTTPException(status_code=404, detail='Topic not found')
    return topic


@topics_router.get('/category/{category_id}')
def get_topic_by_category(category_id: int):
    topic_category = find_topic_by_category(category_id)
    if not topic_category:
        return Response(status_code=404, content='Topic not found')
    return topic_category


@topics_router.post('/new_topic')
def create_new_topic(title: str, content: str, user_id: int, category_id: int):
    new_topic = create_topic(title, content, user_id, category_id)

    return new_topic


@topics_router.delete('/{topic_id}')
def delete_topic(topic_id: int):
    topic = find_topic_by_id(topic_id)
    if not topic:
        return Response(status_code=404)

    topics.remove(topic)

    return Response(status_code=204)
