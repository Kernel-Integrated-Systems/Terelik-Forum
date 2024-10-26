from fastapi import APIRouter, Response, HTTPException, Header, Body
from pydantic import BaseModel

from modules.categories import Category, NewCategory
from services.categories_services import create_category, find_category_by_id, remove_category, view_categories
from services.user_services import authenticate, decode_jwt_token, grant_write_access, revoke_access, grant_read_access, \
    get_user_accessible_categories, get_access_level

categories_router = APIRouter(prefix='/categories', tags=["Categories"])




@categories_router.get('/')
def show_categories(authorization: str | None = Header(None)):
    # Authenticate and extract user details
    if not authenticate(authorization):
        raise HTTPException(status_code=401, detail="Authorization token missing or invalid")

    token = authorization.split(" ")[1]
    user_info = decode_jwt_token(token)
    user_id = user_info["user_id"]
    user_role = user_info["user_role"]

    try:
        # Admin can see all categories without restriction
        if user_role == 2:  # Admin role
            return list(view_categories())  # Convert to list to avoid generator issues

        # For basic users, retrieve accessible categories
        unlocked_categories = list(view_categories(is_locked=False))
        accessible_locked_categories = list(get_user_accessible_categories(user_id))

        # Combine unlocked and accessible locked categories
        accessible_categories = unlocked_categories + accessible_locked_categories

        return accessible_categories

    except ValueError as e:
        return Response(status_code=400, content=str(e))

@categories_router.get('/{category_id}')
def get_category_by_id(category_id: int, authorization: str | None = Header(None)):
    if not authenticate(authorization):
        raise HTTPException(status_code=401, detail="Authorization token missing or invalid")

    token = authorization.split(" ")[1]

    user_info = decode_jwt_token(token)
    user_id = user_info["user_id"]
    user_role = user_info["user_role"]

    if user_role == 2 or get_access_level(user_id, category_id) in [1, 2]:
        try:
            return find_category_by_id(category_id)
        except ValueError as e:
            return Response(status_code=404, content=str(e))

    raise HTTPException(status_code=403, detail="You do not have permission to view this category")


@categories_router.post('/')
def create_new_category(category: NewCategory, authorization: str | None = Header(None)):
    if not authenticate(authorization):
        raise HTTPException(status_code=401, detail="Authorization token missing or invalid")

    token = authorization.split(" ")[1]
    user_info = decode_jwt_token(token)
    user_role = user_info["user_role"]

    if user_role != 2:
        raise HTTPException(status_code=403, detail="You do not have permission to create categories")

    try:
        # Pass is_private and is_locked to the create_category function
        return create_category(category.category_name, category.is_private, category.is_locked)
    except ValueError as e:
        return Response(status_code=400, content=str(e))



@categories_router.delete('/{category_id}')
def delete_category(category_id: int, authorization: str | None = Header(None)):
    if not authenticate(authorization):
        raise HTTPException(status_code=401, detail="Authorization token missing or invalid")

    token = authorization.split(" ")[1]
    user_info = decode_jwt_token(token)
    user_role = user_info["user_role"]

    if user_role != 2:
        raise HTTPException(status_code=403, detail="You do not have permission to delete categories")

    try:
        return remove_category(category_id)
    except ValueError as e:
        return Response(status_code=404, content=str(e))

