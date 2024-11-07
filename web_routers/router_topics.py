from fastapi import APIRouter, Request, Form, Depends
from starlette.templating import Jinja2Templates
from typing import List, Dict
from modules.users import User
from services import user_services as us
from services import topic_services as ts
from services import categories_services as cs

topics_router = APIRouter(prefix='/topics')
templates = Jinja2Templates(directory='templates')

@topics_router.get('')
def display_topics(request: Request):
    # Obtain logged in user
    token = request.cookies.get('token')
    user = us.get_token_user(token)
    topics = ts.view_topics()

    return templates.TemplateResponse(
        request=request,
        name='topics.html',
        context={
            'request': request,
            'topics': topics,
            'user': user
        }
    )

def map_topic_replies_and_authors(topics, users) -> (Dict[int, List], Dict[int, User], Dict[int, User]):
    # Map user ID to User object
    user_map = {usr.id: usr for usr in users}

    # Initialize maps
    topic_replies_map = {}
    reply_author_map = {}
    author_map = {}

    for tpc in topics:
        # Retrieve the topic with replies for each topic ID
        full_topic = ts.find_topic_by_id(tpc.topic_id)
        topic_replies_map[tpc.topic_id] = full_topic.replies

        # Map each reply's user_id to User object
        for reply in full_topic.replies:
            reply_author_map[reply.user_id] = user_map.get(reply.user_id)

        # Map the topic author using user_map
        author_map[tpc.topic_id] = user_map.get(tpc.user_id)

    return topic_replies_map, reply_author_map, author_map


@topics_router.get('/{topic_id}')
def display_topic_details(request: Request, topic_id: int):
    # Obtain logged in user
    token = request.cookies.get('token')
    user = us.get_token_user(token)
    # Filer topic data
    selected_topic = ts.find_topic_by_id(topic_id)
    all_topics = ts.view_topics()
    topics = [topic for topic in all_topics if topic.category_id == 1]

    if not user:
        public_categories = cs.show_public_categories()
        public_category_ids = {cat.category_id for cat in public_categories}
        topics = [tpc for tpc in topics if tpc.category_id in public_category_ids]

    # Call all topic authors and map usr id with User()
    users = us.get_all_users()
    topic_replies_map, reply_author_map, author_map = map_topic_replies_and_authors(topics, users)

    return templates.TemplateResponse(
        request=request,
        name='single_topic.html',
        context={
            'request': request,
            'topics': topics,
            'topic': selected_topic,
            'author_map': author_map,
            'reply_author_map': reply_author_map,
            'topic_replies_map': topic_replies_map,
            'user': user
        }
    )

# Create Topic Utility function
def _get_new_topic_data(
    title: str = Form(...),
    content: str = Form(...),
    category_id: int = Form(...),
    locked: bool = Form(False)
):
    return title, content, category_id, locked

# Handle submit new topic request and redirect Topics page
@topics_router.post('')
def create_topic(request: Request, form_data: tuple = Depends(_get_new_topic_data)):
    # Obtain logged in user
    token = request.cookies.get('token')
    user = us.get_token_user(token)
    title, content, category_id, locked = form_data

    is_locked = 1 if locked else 0

    try:
        new_topic = ts.create_topic(title, content, user.id, category_id, is_locked)
        topics = ts.view_topics()
        # Call all topic authors and map usr id with User()
        users = us.get_all_users()
        topic_replies_map, reply_author_map, author_map = map_topic_replies_and_authors(topics, users)

        return templates.TemplateResponse(
            request=request,
            name='single_topic.html',
            context={
                'request': request,
                'topics': topics,
                'topic': new_topic,
                'author_map': author_map,
                'reply_author_map': reply_author_map,
                'topic_replies_map': topic_replies_map,
                'user': user
            }
        )
    except ValueError as e:
        return templates.TemplateResponse(
            request=request,
            name='topics.html',
            context={
                "request": request,
                "error": str(e),
                'user': user
            })

    except Exception as e:
        return templates.TemplateResponse(
            request=request,
            name='topics.html',
            context={
                "request": request,
                "error": str(e),
                'user': user
            })