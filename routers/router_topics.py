from fastapi import APIRouter, Response, HTTPException, Header
from services.categories_services import find_category_by_id
from services.topic_services import (view_topics, create_topic, find_topic_by_id, find_topic_by_category, remove_topic,
                                     change_topic_lock_status)
from services.user_services import authenticate, authorise_user_role

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
def create_new_topic(title: str, content: str, user_id: int, category_id: int):
    category = find_category_by_id(category_id)
    if category.locked == 1:
        return Response(status_code=400, content=f'Category {category_id} is locked.')
    try:
        return create_topic(title, content, user_id, category_id)
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
    if not authenticate(token):
        raise HTTPException(status_code=401, detail="Authorization token missing or invalid")
    user_role = authorise_user_role(token)
    if user_role["user_role"] != 2:
        raise HTTPException(status_code=401, detail="Unauthorized access. You are not admin!")
    try:
        return change_topic_lock_status(topic_id)
    except ValueError as e:
        return Response(status_code=404, content=str(e))
