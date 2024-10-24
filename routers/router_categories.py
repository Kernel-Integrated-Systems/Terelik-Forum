from fastapi import APIRouter, Response, HTTPException, Header, Body

from modules.categories import Category, NewCategory
from services.categories_services import view_categories, find_category_by_id, create_category, remove_category
from services.user_services import authenticate, decode_jwt_token, grant_read_access, grant_write_access, \
    authorise_user_role

categories_router = APIRouter(prefix='/categories', tags=["Categories"])


@categories_router.get('/')
def show_categories():
    try:
        return view_categories()
    except ValueError as e:
        return Response(status_code=400, content=str(e))


@categories_router.get('/{category_id}')
def get_category_by_id(category_id: int):
    try:
        return find_category_by_id(category_id)
    except ValueError as e:
        return Response(status_code=404, content=str(e))


@categories_router.post('/')
def create_new_category(category: NewCategory, token: str | None = Header()):
    # Check if user is authenticated
    if not authenticate(token):
        raise HTTPException(status_code=401, detail="Authorization token missing or invalid")
    # Validate user role is admin and raise error if not
    user_role = authorise_user_role(token)
    if user_role["user_role"] != 2:
        raise HTTPException(status_code=401, detail="Unauthorized access. You need to be admin!")
    try:
        return create_category(category.category_name)
    except ValueError as e:
        return Response(status_code=400, content=str(e))


@categories_router.delete('/{category_id}')
def delete_category(category_id: int, token: str | None = None):
    # Check if user is authenticated
    if not authenticate(token):
        raise HTTPException(status_code=401, detail="Authorization token missing or invalid")
    # Validate user role is admin and raise error if not
    user_role = authorise_user_role(token)
    if user_role["user_role"] != 2:
        raise HTTPException(status_code=401, detail="Unauthorized command. You are not admin!")
    try:
        return remove_category(category_id)
    except ValueError as e:
        return Response(status_code=404, content=str(e))

