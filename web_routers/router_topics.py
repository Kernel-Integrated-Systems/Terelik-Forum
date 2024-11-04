from lib2to3.fixes.fix_input import context

from fastapi import APIRouter, Request
from starlette.templating import Jinja2Templates
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

@topics_router.get('/{topic_id}')
def display_topic_details(request: Request, topic_id: int):
    # Obtain logged in user
    token = request.cookies.get('token')
    user = us.get_token_user(token)
    # Filer topic data
    selected_topic = ts.find_topic_by_id(topic_id)
    topics = ts.view_topics()
    if not user:
        public_categories = cs.show_public_categories()
        public_category_ids = {cat.category_id for cat in public_categories}
        topics = [tpc for tpc in topics if tpc.category_id in public_category_ids]

    return templates.TemplateResponse(
        request=request,
        name='single_topic.html',
        context={
            'request': request,
            'topics': topics,
            'topic': selected_topic,
            'user': user
        }
    )