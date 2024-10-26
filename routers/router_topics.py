from fastapi import APIRouter, Response, Header, HTTPException

from services.topic_services import (view_topics, create_topic, find_topic_by_id, find_topic_by_category, remove_topic)
from services.user_services import authenticate, decode_jwt_token

topics_router = APIRouter(prefix='/topics', tags=['Topics'])


@topics_router.get('/')
def get_topics(authorization: str = Header(...)):
    if not authenticate(authorization):
        raise HTTPException(status_code=401, detail="Authorization token missing or invalid")

    return view_topics()


@topics_router.get('/{topic_id}')
def get_topic_by_id(topic_id: int, authorization: str = Header(...)):
    if not authenticate(authorization):
        raise HTTPException(status_code=401, detail="Authorization token missing or invalid")

    try:
        return find_topic_by_id(topic_id)
    except ValueError as e:
        return Response(status_code=400, content=str(e))


@topics_router.get('/category/{category_id}')
def get_topic_by_category(category_id: int, authorization: str = Header(...)):
    if not authenticate(authorization):
        raise HTTPException(status_code=401, detail="Authorization token missing or invalid")

    try:
        return find_topic_by_category(category_id)
    except ValueError as e:
        return Response(status_code=400, content=str(e))


@topics_router.post('/new_topic')
def create_new_topic(title: str, content: str, user_id: int, category_id: int, authorization: str = Header(...)):
    if not authenticate(authorization):
        raise HTTPException(status_code=401, detail="Authorization token missing or invalid")

    token_data = decode_jwt_token(authorization.split(" ")[1])
    if token_data["user_id"] != user_id:
        raise HTTPException(status_code=403, detail="You cannot create topics on behalf of another user.")

    try:
        return create_topic(title, content, user_id, category_id)
    except ValueError as e:
        return Response(status_code=400, content=str(e))


@topics_router.delete('/{topic_id}')
def delete_topic(topic_id: int, authorization: str = Header(...)):
    if not authenticate(authorization):
        raise HTTPException(status_code=401, detail="Authorization token missing or invalid")

    try:
        return remove_topic(topic_id)
    except ValueError as e:
        return Response(status_code=400, content=str(e))
