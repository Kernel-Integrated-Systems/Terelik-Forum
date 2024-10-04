from fastapi import APIRouter, HTTPException, Response

from services.topic_services import (view_topics, create_topic, find_topic_by_id,
                                     find_topic_by_title, find_topic_by_category, post_new_topic)
from percistance.data import topics

topics_router = APIRouter(prefix='/topics')


@topics_router.get('/topics')
def get_topics():
    return view_topics()


@topics_router.get('/topics/{topic_id}')
def get_topic_by_id(topic_id: int):
    topic = find_topic_by_id(topic_id)
    if not topic:
        raise HTTPException(status_code=404, detail='Topic not found')
    return topic


@topics_router.get('/topics/title')
def get_topic_by_title(title: str):
    topic = find_topic_by_title(title)
    if not topic:
        raise HTTPException(status_code=404, detail='Topic not found')
    return topic


@topics_router.get('/topics/{category}')
def get_topic_by_category(category: str):
    topic = find_topic_by_category(category)
    if not topic:
        raise HTTPException(status_code=404, detail='Topic not found')
    return topic


@topics_router.post('/topics/new_topic')
def create_new_topic(id: int, title: str, category: str):
    try:
        new_topic = post_new_topic(id, title, category)
        return new_topic
    except ValueError as err:
        raise HTTPException(status_code=400, detail=str(err))


@topics_router.delete('/topics/{topic_id}')
def delete_topic(topic_id: int):
    topic = find_topic_by_id(topic_id)
    if not topic:
        return Response(status_code=404)

    topics.remove(topic)

    return Response(status_code=204)
