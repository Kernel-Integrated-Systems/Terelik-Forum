from fastapi import APIRouter, HTTPException, Response
from services.categories_services import create_category, find_category_by_id_f, view_categories
from percistance.data import categories

categories_router = APIRouter(prefix='/categories')


@categories_router.get('/')
def show_categories():
    return view_categories()


@categories_router.post('/')
def create_new_category(category_name: str):
    category = create_category(category_name)
    return category


@categories_router.get('/{category_id}')
def find_category_by_id(category_id: int):
    category = find_category_by_id_f(category_id)
    if not category:
        return Response(status_code=404, content='Category not found')
    return category


@categories_router.delete('/{category_id}')
def delete_category(category_id: int):
    category = find_category_by_id_f(category_id)
    if not category:
        return Response(status_code=404)

    categories.remove(category)

    return Response(status_code=204)
