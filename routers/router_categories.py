from fastapi import APIRouter, Response
from services.categories_services import create_category, find_category_by_id, view_categories, remove_category

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
def create_new_category(category_name: str):
    try:
        return create_category(category_name)
    except ValueError as e:
        return Response(status_code=400, content=str(e))


@categories_router.delete('/{category_id}')
def delete_category(category_id: int):
    try:
        return remove_category(category_id)
    except ValueError as e:
        return Response(status_code=404, content=str(e))

