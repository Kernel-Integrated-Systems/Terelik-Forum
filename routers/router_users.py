from fastapi import APIRouter, HTTPException, Response, Header
from modules.users import UserRegistrationRequest
from percistance.data import authenticate
from services.user_services import get_all_users, get_user_by_id, register_user, authenticate_user, un_authenticate_user

users_router = APIRouter(prefix='/users', tags=['Users'])


@users_router.get('/')
def get_all_users_route(token: str | None = None):
    if not authenticate(token):
        raise HTTPException(status_code=401, detail="Authorization token missing or invalid")

    try:
        return get_all_users()
    except ValueError as e:
        return Response(content=str(e), status_code=400)

@users_router.get('/{user_id}')
def get_user_route(user_id: int, token: str | None = None):
    if not authenticate(token):
        raise HTTPException(status_code=401, detail="Authorization token missing or invalid")

    try:
        # Pass the token to get_user_by_id() function
        return get_user_by_id(user_id)
    except ValueError as e:
        return Response(content=str(e), status_code=400)


@users_router.post('/register')
def register_user_route(
        username: str = Header(..., description="The username of the user"),
        email: str = Header(..., description="The email of the user"),
        password: str = Header(..., description="The password of the user")
):
    try:
        # Manually create the UserRegistrationRequest model
        user_request = UserRegistrationRequest(username=username, email=email, password=password)

        # Pass the model to the register_user function
        return register_user(user_request.username, user_request.email, user_request.password)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@users_router.post('/login')
def login_user_route(username: str, password: str):
    try:
        return authenticate_user(username, password)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@users_router.post('/lgout')
def logout_user_route(username: str, token: str | None = None):
    if not authenticate(token):
        raise HTTPException(status_code=401, detail="Authorization token missing or invalid")

    try:
        return un_authenticate_user(username)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
