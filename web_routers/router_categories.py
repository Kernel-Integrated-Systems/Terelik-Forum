from fastapi import APIRouter, Request, Form, Depends
from starlette.templating import Jinja2Templates
from services import categories_services as cs
from services import user_services as us


categories_router = APIRouter(prefix='/categories')
templates = Jinja2Templates(directory='templates')

@categories_router.get('')
def display_categories(request: Request):
    token = request.cookies.get('token')
    user = us.get_token_user(token)
    categories = list(cs.view_categories())
    if not user:
        categories = [cat for cat in categories if cat.private == 0]

    return templates.TemplateResponse(
        request=request,
        name='categories.html',
        context={
            'request': request,
            'categories': categories,
            'user': user}
    )

@categories_router.get('/{category_id}')
def display_category_details(request: Request, category_id: int):
    selected_category = cs.find_category_by_id(category_id)
    categories = list(cs.view_categories())

    token = request.cookies.get('token')
    print(token)
    user = us.get_token_user(token)

    return templates.TemplateResponse(
        request=request,
        name='single_category.html',
        context={
            'request': request,
            'categories': categories,
            'category': selected_category,
            'user': user}
    )


# Utility function
def _get_new_category_data(
    title: str = Form(...),
    private: bool = Form(False),
    locked: bool = Form(False)
):
    return title, private, locked

# Handle submit new category request and redirect Categories page
@categories_router.post('')
def create_category(request: Request, form_data: tuple = Depends(_get_new_category_data)):
    categories = list(cs.view_categories())
    title, private, locked = form_data
    is_private = 1 if private else 0
    is_locked = 1 if locked else 0
    try:
        new_category = cs.create_category(title, is_private, is_locked)
        return templates.TemplateResponse(
            request=request,
            name='single_category.html',
            context={
                'request': request,
                'categories': categories,
                'category': new_category}
        )
    except ValueError as e:
        return templates.TemplateResponse(
            request=request,
            name='categories.html',
            context={
                "request": request,
                "error": str(e)
            })

    except Exception as e:
        return templates.TemplateResponse(
            request=request,
            name='categories.html',
            context={
                "request": request,
                "error": str(e)
            })