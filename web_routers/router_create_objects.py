from fastapi import APIRouter, Request
from starlette.templating import Jinja2Templates
from services import user_services as us

create_router = APIRouter(prefix='/create')
templates = Jinja2Templates(directory='templates')


# Display Create Category form
@create_router.get('/new_category')
def create_new_category_form(request: Request):
    token = request.cookies.get('token')
    user = us.get_token_user(token)
    return templates.TemplateResponse(
        request=request,
        name='create_category.html',
        context={
            'request': request,
            'user': user}
    )

# Display Create Topic form
@create_router.get('/new_topic')
def create_new_topic_form(request: Request):
    token = request.cookies.get('token')
    user = us.get_token_user(token)
    return templates.TemplateResponse(
        request=request,
        name='create_topic.html',
        context={
            'request': request,
            'user': user
        }
    )
