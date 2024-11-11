
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates

from models.replies import BestReply
from services import topic_services
from services.categories_services import view_categories
from services.replies_services import get_replies_with_vote_counts
from fastapi import APIRouter, Response, HTTPException, Request, Form
from services.topic_services import view_categories_with_topics
from services.user_services import authenticate

topics_router = APIRouter(prefix='/topics', tags=['Topics'])
templates = Jinja2Templates(directory="templates")

@topics_router.get("/by_category")
def get_topics_by_category(
        request: Request,
        category_id: int,
        page: int = 1,
        page_size: int = 4
):
    try:
        topics = topic_services.find_topic_by_category(category_id)
        categories = view_categories()
        start_index = (page - 1) * page_size
        paginated_topics = topics[start_index:start_index + page_size] if topics else []

        return templates.TemplateResponse("topics_per_cat.html", {
            "request": request,
            "topics": paginated_topics,
            "categories": categories,
            "category_id": category_id,
            "page": page,
            "page_size": page_size
        })
    except ValueError:
        categories = view_categories()
        return templates.TemplateResponse("topics_per_cat.html", {
            "request": request,
            "topics": [],
            "categories": categories,
            "category_id": category_id,
            "page": page,
            "page_size": page_size,
            "no_topics_message": "No topics in this category."
        })

@topics_router.get("/", response_class=HTMLResponse)
def show_all_topics(request: Request):
    try:
        categories = view_categories_with_topics()  # Use the function that includes topics
        return templates.TemplateResponse("all_topics.html", {"request": request, "categories": categories})
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@topics_router.get("/new", response_class=HTMLResponse)
def show_create_topic_page(request: Request):
    categories = view_categories()
    return templates.TemplateResponse("create_topic.html", {"request": request, "categories": categories})

@topics_router.get("/{topic_id}")
def get_topic_with_replies(request: Request, topic_id: int):
    try:
        topic = topic_services.find_topic_by_id(topic_id)
        replies_with_votes = get_replies_with_vote_counts(topic_id)
        categories = view_categories()

        return templates.TemplateResponse("topic.html", {
            "request": request,
            "topic": topic,
            "replies": replies_with_votes,
            "categories": categories
        })
    except ValueError:
        return Response(status_code=404, content="Topic not found.")



@topics_router.get("/new", response_class=HTMLResponse)
def show_create_topic_page(request: Request):
    categories = view_categories()
    return templates.TemplateResponse("create_topic.html", {"request": request, "categories": categories})



@topics_router.post("/new")
def create_new_topic(
        title: str = Form(...),
        content: str = Form(...),
        category_id: int = Form(...),
        request: Request = None,
):
    user_data = authenticate(request)
    user_id = user_data["user_id"]

    try:
        return topic_services.create_topic(title, content, user_id, category_id)
    except ValueError as e:
        return templates.TemplateResponse("create_topic.html", {"request": request, "error": str(e)})


# Choose Best Reply
@topics_router.post('/{topic_id}/replies{reply_id}')
def select_best_reply(reply: BestReply, request: Request = None):
    user_data = authenticate(request)
    if not user_data:
        raise HTTPException(status_code=401, detail="Authorization token missing or invalid")

    try:
        return topic_services.choose_best_reply(reply.topic_id, reply.reply_id, user_data["user_id"])
    except ValueError as e:
        return Response(status_code=400, content=str(e))

@topics_router.delete('/{topic_id}')
def delete_topic(topic_id: int, request: Request = None):
    user_data = authenticate(request)

    if user_data["user_role"] == 1:
        raise HTTPException(status_code=403, detail="You do not have permission to grant access")

    try:
        return topic_services.remove_topic(topic_id)
    except ValueError as e:
        return Response(status_code=400, content=str(e))

@topics_router.post('/change_topic_lock_status')
def change_lock_status(topic_id: int, request: Request = None):
    user_data = authenticate(request)
    user_role = user_data["user_role"]
    if user_role == 1:
        raise HTTPException(status_code=403, detail="You do not have permission to grant access")

    try:
        return topic_services.change_topic_lock_status(topic_id)
    except ValueError as e:
        return Response(status_code=404, content=str(e))