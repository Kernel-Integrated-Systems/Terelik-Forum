from fastapi import APIRouter, HTTPException, Response, Header, Body
from modules.users import UserRegistrationRequest, UserLoginRequest, UserAccess
from services.user_services import get_all_users, get_user_by_id, register_user, authenticate, \
    grant_read_access, grant_write_access, revoke_access, \
    logout_user, authenticate_user

users_router = APIRouter(prefix='/users', tags=['Users'])


@users_router.get('/')
def get_all_users_route(authorization: str = Header(...)):
    # Check if user is authenticated
    user_data = authenticate(authorization)
    if not user_data:
        raise HTTPException(status_code=401, detail="Authorization token missing or invalid")
    try:
        return get_all_users()
    except ValueError as e:
        return Response(content=str(e), status_code=400)

@users_router.get('/{user_id}')
def get_user_route(user_id: int, authorization: str = Header(...)):
    user_info = authenticate(authorization)
    try:
        # Pass the token to get_user_by_id() function
        return get_user_by_id(user_id)
    except ValueError as e:
        return Response(content=str(e), status_code=400)


@users_router.post('/register')
def register_user_route(new_usr: UserRegistrationRequest):
    try:
        # Manually create the UserRegistrationRequest model
        user_request = UserRegistrationRequest(
            username=new_usr.username,
            email=new_usr.email,
            password=new_usr.password
        )

        # Pass the model to the register_user function
        return register_user(user_request.username, user_request.email, user_request.password)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@users_router.post('/login')
def login_user_route(user: UserLoginRequest):
    try:
        return authenticate_user(user.username, user.password)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

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