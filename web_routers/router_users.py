from fastapi import APIRouter, Request, Form, Depends
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse, Response
from services import user_services


users_router = APIRouter(prefix='/users')
templates = Jinja2Templates(directory='templates')

# Display Login as guest
@users_router.get('/login')
def display_login(request: Request):
    return templates.TemplateResponse(request=request, name='login.html')

# Handle Login submission
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

# Display Register as guest
@users_router.get('/register')
def display_register(request: Request):
    return templates.TemplateResponse(request=request, name='register.html')


def _get_registration_form_data(
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...)
):
    return username, email, password

# Handle Register submission
@users_router.post('/register')
def register(request: Request, form_data: tuple = Depends(_get_registration_form_data)):
    # Verify username and password
    username, email, password = form_data

    try:
        # Attempt to register the user
        user_services.register_user(username, email, password)
        token = user_services.authenticate_user(username, password)
        response = RedirectResponse(url='/', status_code=302)
        response.set_cookie('token', token)
        return response

    except ValueError as e:
        return templates.TemplateResponse(
            request=request,
            name='register.html',
            context={
                "request": request,
                "error": str(e)
            })

    except Exception as e:
        return templates.TemplateResponse(
            request=request,
            name='register.html',
            context={
                "request": request,
                "error": str(e)
            })


@users_router.post('/logout')
def handle_logout(request: Request):
    token = request.cookies.get('token')
    user = user_services.get_token_user(token)
    if user:
        response = RedirectResponse(url='/', status_code=302)
        response.delete_cookie('token')
        return response
    else:
        return RedirectResponse(url='/', status_code=302)

