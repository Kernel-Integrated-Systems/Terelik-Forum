from fastapi import APIRouter, Header
from starlette.templating import Jinja2Templates

from models.users import UserAccess
from services.user_services import register_user, authenticate, grant_read_access, grant_write_access, revoke_access, logout_user


from fastapi import APIRouter, HTTPException, Response, Form, Request
from starlette.responses import RedirectResponse, JSONResponse
from starlette.templating import Jinja2Templates
from services.user_services import authenticate_user, create_jwt_token, get_user_by_credentials

users_router = APIRouter(prefix='/users', tags=['Users'])
templates = Jinja2Templates(directory="templates")

@users_router.get("/login")
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@users_router.post("/login")
def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...)
):
    user = get_user_by_credentials(username, password)
    if not user:
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error_message": "Invalid username or password"}
        )

    token = create_jwt_token(user_id=user.id, username=user.username, user_role=user.role)

    response = RedirectResponse(url="/", status_code=302)
    response.set_cookie(key="access_token", value=token, httponly=True, samesite="Lax")
    return response



@users_router.get("/register")
def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@users_router.post("/register")
def register_user_route(
        request: Request,
        username: str = Form(...),
        email: str = Form(...),
        password: str = Form(...)
):
    try:
        register_user(username, email, password)
        return RedirectResponse(url="/users/login", status_code=303)
    except ValueError as e:
        return templates.TemplateResponse(
            "register.html",
            {"request": request, "error_message": str(e)}
        )


@users_router.get('/id/{user_id}')
def get_user_route(user_id: int, authorization: str = Header(...)):

    return {"user_id": user_id}

@users_router.post('/logout')
def logout_user_route(authorization: str = Header(...)):
    if not authenticate(authorization):
        raise HTTPException(status_code=401, detail="Authorization token missing or invalid")
    token = authorization.split(" ")[1]

    try:
        response = logout_user(token)
        return response
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@users_router.post('/grant_read_access/')
def give_user_read_access(user: UserAccess, authorization: str = Header(...)):
    user_info = authenticate(authorization)
    if not user_info:
        raise HTTPException(status_code=401, detail="Authorization token missing or invalid")

    if user_info["user_role"] == 1:
        raise HTTPException(status_code=403, detail="You do not have permission to grant access")

    try:
        return grant_read_access(user.user_id, user.category_id)
    except ValueError as e:
        return Response(status_code=400, content=str(e))



@users_router.post('/grant_write_access/')
def give_user_write_access(user: UserAccess, authorization: str = Header(...)):
    user_info = authenticate(authorization)
    if not user_info:
        raise HTTPException(status_code=401, detail="Authorization token missing or invalid")

    if user_info["user_role"] == 1:
        raise HTTPException(status_code=403, detail="You do not have permission to grant access")

    try:
        return grant_write_access(user.user_id, user.category_id)
    except ValueError as e:
        return Response(status_code=400, content=str(e))


@users_router.post('/revoke_access')
def revoke_user_access(user: UserAccess, authorization: str = Header(...)):
    user_info = authenticate(authorization)
    if user_info["user_role"] != 2:
        raise HTTPException(status_code=403, detail="You do not have permission to revoke access")

    try:
        return revoke_access(user.user_id,user.category_id)
    except ValueError as e:
        return Response(status_code=400, content=str(e))


