from fastapi import APIRouter, HTTPException, Response
from modules.users import User, UserRegistrationRequest, UserLoginRequest
from services.user_services import get_all_users, get_user_by_id, register_user, authenticate_user

users_router = APIRouter(prefix='/users', tags=['Users'])


@users_router.get('/')
def get_all_users_route():
    try:
        return get_all_users()
    except ValueError as e:
        return Response(content=str(e), status_code=400)

@users_router.get('/{user_id}')
def get_user_route(user_id: int):
    try:
        return get_user_by_id(user_id)
    except ValueError as e:
        return Response(content=str(e), status_code=400)

@users_router.post('/register')
def register_user_route(user: UserRegistrationRequest):
    try:
        return register_user(user.username, user.email, user.password)
    except ValueError as err:
        raise HTTPException(status_code=400, detail=str(err))


@users_router.post('/login')
def login_user_route(username: str, password: str):
    try:
        return authenticate_user(username, password)
    except ValueError as err:
        raise HTTPException(status_code=400, detail=str(err))

