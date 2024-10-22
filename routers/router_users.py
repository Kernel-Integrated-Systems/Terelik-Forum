import jwt
from fastapi import APIRouter, HTTPException, Response, Header, Body
from pydantic import BaseModel

from modules.users import UserRegistrationRequest, UserLoginRequest
from services.user_services import get_all_users, get_user_by_id, register_user, authenticate_user, \
    un_authenticate_user, authenticate, decode_jwt_token, grant_read_access, grant_write_access, revoke_access

users_router = APIRouter(prefix='/users', tags=['Users'])

@users_router.get('/')
def get_all_users_route(authorization: str | None = Header(None)):
    if not authorization or not authenticate(authorization):
        raise HTTPException(status_code=401, detail="Authorization token missing or invalid")

    try:
        return get_all_users()
    except ValueError as e:
        return Response(content=str(e), status_code=400)

@users_router.get('/{user_id}')
def get_user_route(user_id: int, authorization: str | None = Header(None)):
    if not authorization or not authenticate(authorization):
        raise HTTPException(status_code=401, detail="Authorization token missing or invalid")

    try:
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
        user_request = UserRegistrationRequest(username=username, email=email, password=password)
        return register_user(user_request.username, user_request.email, user_request.password)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@users_router.post('/login')
def login_user_route(user: UserLoginRequest):
    try:
        user_info = authenticate_user(user.username, user.password)
        return {
            "access_token": user_info['token'],
            "token_type": user_info['token_type']
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@users_router.post('/logout')
def logout_user_route(username: str, authorization: str | None = Header(None)):
    if not authorization or not authenticate(authorization):
        raise HTTPException(status_code=401, detail="Authorization token missing or invalid")

    try:
        return un_authenticate_user(username)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))



@users_router.post('/grant_read_access/')
def give_user_read_access(body: dict = Body(...), authorization: str = Header(None)):
    if not authenticate(authorization):
        raise HTTPException(status_code=401, detail="Authorization token missing or invalid")

    token = authorization.split(" ")[1]
    user_info = decode_jwt_token(token)
    user_role = user_info["user_role"]

    if user_role != 2:
        raise HTTPException(status_code=403, detail="You do not have permission to grant access")

    user_id = body.get("user_id")
    category_id = body.get("category_id")

    if user_id is None or category_id is None:
        raise HTTPException(status_code=400, detail="user_id and category_id are required")

    try:
        return grant_read_access(user_id, category_id)
    except ValueError as e:
        return Response(status_code=400, content=str(e))



@users_router.post('/grant_write_access/')
def give_user_write_access(body: dict = Body(...), authorization: str = Header(None)):
    if not authenticate(authorization):
        raise HTTPException(status_code=401, detail="Authorization token missing or invalid")

    token = authorization.split(" ")[1]
    user_info = decode_jwt_token(token)
    user_role = user_info["user_role"]

    if user_role != 2:
        raise HTTPException(status_code=403, detail="You do not have permission to grant access")

    user_id = body.get("user_id")
    category_id = body.get("category_id")

    if user_id is None or category_id is None:
        raise HTTPException(status_code=400, detail="user_id and category_id are required")

    try:
        return grant_write_access(user_id, category_id)
    except ValueError as e:
        return Response(status_code=400, content=str(e))



class RevokeAccessRequest(BaseModel):     #not sure about this
    user_id: int
    category_id: int
    access_type: str
@users_router.post('/revoce_access/') #still not fully tested
def revoke_user_access(request: RevokeAccessRequest, authorization: str = Header(None)):

    if not authenticate(authorization):
        raise HTTPException(status_code=401, detail="Authorization token missing or invalid")

    token = authorization.split(" ")[1]
    user_info = decode_jwt_token(token)
    user_role = user_info["user_role"]

    if user_role != 2:
        raise HTTPException(status_code=403, detail="You do not have permission to revoke access")

    if request.access_type not in ["read", "write"]:
        raise HTTPException(status_code=400, detail="Invalid access type. Must be 'read' or 'write'.")

    try:
        revoke_access(request.user_id, request.category_id, request.access_type)
        return {"message": f"User {request.user_id}'s {request.access_type} access to category {request.category_id} has been revoked."}
    except ValueError as e:
        return Response(status_code=400, content=str(e))