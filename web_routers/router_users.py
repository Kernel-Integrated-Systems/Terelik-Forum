from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse

from services import user_services


users_router = APIRouter(prefix='/users')
templates = Jinja2Templates(directory='templates')

@users_router.get('/login')
def handle_login(request: Request):
    return templates.TemplateResponse(request=request, name='login.html')


@users_router.post('/login')
def login(request: Request, username: str = Form(...), password: str = Form()):
    # Verify username and password
    token = user_services.authenticate_user(username, password)
    if token:
        response = RedirectResponse(url='/', status_code=302)
        response.set_cookie('token', token)
        return response
    else:
        return templates.TemplateResponse(request=request, name='login.html')