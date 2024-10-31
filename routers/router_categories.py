from fastapi import APIRouter, Response, HTTPException, Header
from modules.categories import NewCategory
from services.categories_services import view_categories, find_category_by_id, create_category, remove_category, \
    show_users_on_category
from services.user_services import authenticate, decode_jwt_token, grant_read_access, grant_write_access,  get_user_accessible_categories, get_access_level

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
def create_new_category(category: NewCategory, authorization: str = Header(...)):
    user_info = authenticate(authorization)
    if user_info["user_role"] != 2:
        raise HTTPException(status_code=403, detail="You do not have permission to create categories")

    try:
        return create_category(category.category_name, category.private, category.locked)
    except ValueError as e:
        return Response(status_code=404, content=str(e))

@categories_router.get('/{category_id}')
def get_category_by_id(category_id: int):
    try:
        return find_category_by_id(category_id)
    except ValueError as e:
        return Response(status_code=404, content=str(e))



@categories_router.delete('/{category_id}')
def delete_category(category_id: int, authorization: str = Header(...)):
    user_info = authenticate(authorization)
    if user_info["user_role"] != 2:
        raise HTTPException(status_code=403, detail="You do not have permission to delete categories")

    try:
        return remove_category(category_id)
    except ValueError as e:
        return Response(status_code=404, content=str(e))


@categories_router.get('/{category_id}/privileged_users')
def get_privileged_users_for_category(category_id: int, authorization: str = Header(...)):
    user_info = authenticate(authorization)
    if user_info["user_role"] != 2:
        raise HTTPException(status_code=403, detail="You do not have permission to view privileged users")

    try:
        return show_users_on_category(category_id)
    except ValueError as e:
        return Response(status_code=404, content=str(e))
