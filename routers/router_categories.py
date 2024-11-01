from fastapi import APIRouter, Response, HTTPException, Header, Body

from modules.categories import NewCategory
from services.user_services import authenticate, decode_jwt_token, get_user_accessible_categories, get_access_level
from services.categories_services import create_category, find_category_by_id, view_categories, remove_category, \
    show_users_on_category

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


# @categories_router.post('/change_category_private_status')
# def change_private_status(category_id, token: str | None = Header()):
#     if not authenticate(token):
#         raise HTTPException(status_code=401, detail="Authorization token missing or invalid")
#     user_role = authorise_user_role(token)
#     if user_role["user_role"] != 2:
#         raise HTTPException(status_code=401, detail="Unauthorized access. You are not admin!")
#     try:
#         return change_category_private_status(category_id)
#     except ValueError as e:
#         return Response(status_code=404, content=str(e))
#
#
# @categories_router.post('/change_category_lock_status')
# def change_lock_status(category_id, token: str | None = Header()):
#     if not authenticate(token):
#         raise HTTPException(status_code=401, detail="Authorization token missing or invalid")
#     user_role = authorise_user_role(token)
#     if user_role["user_role"] != 2:
#         raise HTTPException(status_code=401, detail="Unauthorized access. You are not admin!")
#     try:
#         return change_category_lock_status(category_id)
#     except ValueError as e:
#         return Response(status_code=404, content=str(e))
#



@categories_router.get('/{category_id}/privileged_users')
def get_privileged_users_for_category(category_id: int, authorization: str = Header(...)):
    user_info = authenticate(authorization)
    if user_info["user_role"] != 2:
        raise HTTPException(status_code=403, detail="You do not have permission to view privileged users")

    try:
        return show_users_on_category(category_id)
    except ValueError as e:
        return Response(status_code=404, content=str(e))
