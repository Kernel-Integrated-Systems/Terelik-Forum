from fastapi import APIRouter, HTTPException
from modules.users import User, UserRegistrationRequest, UserLoginRequest
from services.user_services import get_all_users, get_user_by_id, register_user, authenticate_user

users_router = APIRouter(prefix='/users')


@users_router.get('/')
def get_all_users_route():
    return get_all_users()


@users_router.get('/{user_id}')
def get_user_route(user_id: int):
    user = get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    return user


@users_router.post('/register')
def register_user_route(user: UserRegistrationRequest):
    try:
        new_user = register_user(user.username, user.email, user.password)
        return new_user
    except ValueError as err:
        raise HTTPException(status_code=400, detail=str(err))



@users_router.post('/login')
def login_user_route(user_login: UserLoginRequest):
    try:
        access_token = authenticate_user(**user_login.dict())
        return {"access token": access_token, "token_type": "bearer"}
    except ValueError as err:
        raise HTTPException(status_code=400, detail=str(err))

