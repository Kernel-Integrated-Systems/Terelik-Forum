from fastapi import APIRouter, Response, HTTPException, Header, Body, Request, Form, Cookie, Depends
from starlette.responses import HTMLResponse, RedirectResponse
from starlette.templating import Jinja2Templates

from models.categories import NewCategory
from services.user_services import authenticate, decode_jwt_token, get_user_accessible_categories, get_access_level, \
    get_current_admin
from services.categories_services import create_category, find_category_by_id, view_categories, remove_category, \
    show_users_on_category, find_category_by_name

categories_router = APIRouter(prefix='/categories', tags=["Categories"])

templates = Jinja2Templates(directory="templates")

@categories_router.get("/", response_class=HTMLResponse)
def show_categories_page(request: Request):
    user_data = authenticate(request)
    is_admin = user_data["user_role"] == 2
    categories = list(view_categories())

    return templates.TemplateResponse("categories.html", {
        "request": request,
        "categories": categories,
        "is_admin": is_admin
    })


@categories_router.get('/new', response_class=HTMLResponse)
def show_create_category_page(request: Request):
    return templates.TemplateResponse("create_category.html", {"request": request})

@categories_router.post('/new')
def create_new_category(
    category_name: str = Form(...),
    private: bool = Form(False),
    locked: bool = Form(False),
    user_data: dict = Depends(get_current_admin),
):
    try:
        new_category = create_category(category_name, private, locked)
        return RedirectResponse(url="/categories/", status_code=303)
    except ValueError as e:
        return templates.TemplateResponse("create_category.html", {"error": str(e)})

@categories_router.delete('/{category_id}')
def delete_category(category_id: int, authorization: str = Header(...)):
    user_info = authenticate(authorization)
    if user_info["user_role"] != 2:
        raise HTTPException(status_code=403, detail="You do not have permission to delete categories")

    try:
        return remove_category(category_id)
    except ValueError as e:
        return Response(status_code=404, content=str(e))




@categories_router.get('/{category_id}')
def get_category_by_id(category_id: int):
    try:
        return find_category_by_id(category_id)
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


@categories_router.get("/search", response_class=HTMLResponse)
def search_category_page(request: Request, query: str):
    try:
        category = find_category_by_name(query)
        categories = [category] if category else []
        return templates.TemplateResponse("categories.html", {"request": request, "categories": categories})
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

