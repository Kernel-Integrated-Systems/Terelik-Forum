from fastapi import APIRouter, Response, HTTPException, Header, Body

from modules.categories import Category
from percistance.data import authenticate, decode_jwt_token
from services.categories_services import create_category, find_category_by_id, remove_category, \
    grant_read_access, grant_write_access

categories_router = APIRouter(prefix='/categories', tags=["Categories"])

@categories_router.get('/')
def show_categories(authorization: str | None = Header(None)):
    if not authenticate(authorization):
        raise HTTPException(status_code=401, detail="Authorization token missing or invalid")

    token = authorization.split(" ")[1]
    user_info = decode_jwt_token(token)
    user_role = user_info["user_role"]

    if user_role not in [1, 0]:
        raise HTTPException(status_code=403, detail="You do not have permission to view categories")

    try:
        return view_categories_for_user()
    except ValueError as e:
        return Response(status_code=400, content=str(e))

@categories_router.get('/{category_id}')
def get_category_by_id(category_id: int, authorization: str | None = Header(None)):
    if not authenticate(authorization):
        raise HTTPException(status_code=401, detail="Authorization token missing or invalid")

    token = authorization.split(" ")[1]
    user_info = decode_jwt_token(token)
    user_role = user_info["user_role"]

    if user_role not in [0, 1]:
        raise HTTPException(status_code=403, detail="You do not have permission to view this category")

    try:
        return find_category_by_id(category_id)
    except ValueError as e:
        return Response(status_code=404, content=str(e))

@categories_router.post('/')
def create_new_category(category: Category, authorization: str | None = Header(None)):
    if not authenticate(authorization):
        raise HTTPException(status_code=401, detail="Authorization token missing or invalid")

    token = authorization.split(" ")[1]
    user_info = decode_jwt_token(token)
    user_role = user_info["user_role"]

    if user_role != 1:
        raise HTTPException(status_code=403, detail="You do not have permission to create categories")

    try:
        return create_category(category.category_name)
    except ValueError as e:
        return Response(status_code=400, content=str(e))

@categories_router.delete('/{category_id}')
def delete_category(category_id: int, authorization: str | None = Header(None)):
    if not authenticate(authorization):
        raise HTTPException(status_code=401, detail="Authorization token missing or invalid")

    token = authorization.split(" ")[1]
    user_info = decode_jwt_token(token)
    user_role = user_info["user_role"]

    if user_role != 1:
        raise HTTPException(status_code=403, detail="You do not have permission to delete categories")

    try:
        return remove_category(category_id)
    except ValueError as e:
        return Response(status_code=404, content=str(e))


@categories_router.post('/grant_read_access/')
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



@categories_router.post('/grant_write_access/')
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