from fastapi import APIRouter, Request
from starlette.templating import Jinja2Templates
from services import categories_services as cs

categories_router = APIRouter(prefix='/categories')
templates = Jinja2Templates(directory='templates')

@categories_router.get('')
def display_categories(request: Request):
    categories = list(cs.view_categories())
    return templates.TemplateResponse(
        request=request,
        name='categories.html',
        context={'request': request,
         'categories': categories}
    )

@categories_router.get('/{category_id}')
def display_category_details(request: Request, category_id: int):
    selected_category = cs.find_category_by_id(category_id)
    categories = list(cs.view_categories())
    print(categories)

    return templates.TemplateResponse(
        request=request,
        name='single_category.html',
        context={'request': request,
         'categories': categories,
         'category': selected_category}
    )
