from fastapi import APIRouter, Request, Form, Depends, Query
from starlette import status
from starlette.responses import JSONResponse, RedirectResponse
from starlette.templating import Jinja2Templates
from services import categories_services as cs
from services import user_services as us


categories_router = APIRouter(prefix='/categories')
templates = Jinja2Templates(directory='templates')

@categories_router.get('')
def display_categories(request: Request):
    # Obtain logged in user
    token = request.cookies.get('token')
    user = us.get_token_user(token)
    # Filer category data
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
    # Obtain logged in user
    token = request.cookies.get('token')
    user = us.get_token_user(token)
    # Filer category data
    selected_category = cs.find_category_by_id(category_id)
    topics = [tpc for tpc in selected_category.topics]

    if not user and selected_category.private == 1:
        return RedirectResponse(url='/', status_code=302)

    return templates.TemplateResponse(
        request=request,
        name='single_category.html',
        context={
            'request': request,
            'topics': topics,
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
    # Obtain logged in user
    token = request.cookies.get('token')
    user = us.get_token_user(token)
    # Filer category data
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
                'category': new_category,
                'user': user
            }
        )
    except ValueError as e:
        return templates.TemplateResponse(
            request=request,
            name='categories.html',
            context={
                "request": request,
                "error": str(e),
                'user': user
            })

    except Exception as e:
        return templates.TemplateResponse(
            request=request,
            name='categories.html',
            context={
                "request": request,
                "error": str(e),
                'user': user
            })

# Handle DELETE category
@categories_router.post('/{category_id}')
def delete_category(request: Request, category_id: int, action: str = Query(None)):
    token = request.cookies.get('token')
    user = us.get_token_user(token)
    categories = list(cs.view_categories())

    try:
        if action == "delete":
            cs.remove_category(category_id)
            return templates.TemplateResponse(
                "categories.html",
                {"request": request, "categories": categories, "user": user}
            )
        else:
            # Create an HTTPException if action is not "delete"
            error = "Invalid request action."
            response = JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"detail": error}
            )
            return templates.TemplateResponse(
                "categories.html",
                {"request": request, "categories": categories, "user": user, "response": response, "error": error}
            )

    except ValueError as e:
        error = str(e)
        return templates.TemplateResponse(
            "categories.html",
            {"request": request, "error": error, "user": user}
        )

    except Exception as e:
        error = str(e)
        return templates.TemplateResponse(
            "categories.html",
            {"request": request, "error": error, "user": user}
        )