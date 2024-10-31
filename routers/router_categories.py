from fastapi import APIRouter, Response, HTTPException, Header, Body
from modules.categories import Categories, NewCategory
from services.user_services import authenticate
from services import categories_services


categories_router = APIRouter(prefix='/categories', tags=["Categories"])


@categories_router.get('/')
def show_categories():
    try:
        return categories_services.view_categories()
    except ValueError as e:
        return Response(status_code=400, content=str(e))


@categories_router.get('/{category_id}')
def get_category_by_id(category_id: int):
    try:
        return categories_services.find_category_by_id(category_id)
    except ValueError as e:
        return Response(status_code=404, content=str(e))


@categories_router.post('/')
def create_new_category(category: NewCategory, token: str | None = Header()):
    # Check if user is authenticated
    user_data = authenticate(token)
    if not user_data:
        raise HTTPException(status_code=401, detail="Authorization token missing or invalid")
    # Validate user role is admin and raise error if not
    user_role = user_data["user_role"]
    if user_role != 2:
        raise HTTPException(status_code=401, detail="Unauthorized access. You need to be admin!")
    try:
        return categories_services.create_category(category.category_name, category.private, category.locked)
    except ValueError as e:
        return Response(status_code=400, content=str(e))


@categories_router.delete('/{category_id}')
def delete_category(category_id: int, token: str | None = None):
    # Check if user is authenticated
    user_data = authenticate(token)
    if not user_data:
        raise HTTPException(status_code=401, detail="Authorization token missing or invalid")
    # Validate user role is admin and raise error if not
    user_role = user_data["user_role"]
    if user_role["user_role"] != 2:
        raise HTTPException(status_code=401, detail="Unauthorized access. You need to be admin!")
    try:
        return categories_services.remove_category(category_id)
    except ValueError as e:
        return Response(status_code=404, content=str(e))


@categories_router.get('/{category_id}/privileged_users')
def get_privileged_users_for_category(category_id: int, token: str | None = None):
    # Check if user is authenticated
    user_data = authenticate(token)
    if not user_data:
        raise HTTPException(status_code=401, detail="Authorization token missing or invalid")
    # Validate user role is admin and raise error if not
    user_role = user_data["user_role"]
    if user_role != 2:
        raise HTTPException(status_code=401, detail="Unauthorized access. You need to be admin!")
    try:
        return categories_services.show_users_on_category(category_id)
    except ValueError as e:
        return Response(status_code=404, content=str(e))