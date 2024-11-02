from fastapi import APIRouter, Request
from starlette.templating import Jinja2Templates
from services import user_services


index_router = APIRouter(prefix='')
templates = Jinja2Templates(directory='templates')


@index_router.get('/')
def index(request: Request):
    token = request.cookies.get('token')
    if token:
        user = user_services.get_token_user(token)
        print(user)
        return templates.TemplateResponse(request=request, name='index.html',
                                          context={'request': request, 'user': user})

    else:
        return templates.TemplateResponse(request=request, name='index.html')