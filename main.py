from fastapi import FastAPI, Request
from starlette.responses import HTMLResponse
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from routers.router_categories import categories_router
from routers.router_topics import topics_router
from routers.router_replies import replies_router, votes_router, best_reply_router
from routers.router_messages import messages_router
from routers.router_users import users_router
from data.database import database_init
from services.categories_services import view_categories
from services.topic_services import view_topics

database_init()

app = FastAPI()

app.include_router(replies_router)
app.include_router(votes_router)
app.include_router(topics_router)
app.include_router(users_router)
app.include_router(messages_router)
app.include_router(best_reply_router)
app.include_router(categories_router)


templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def homepage(request: Request):
    categories = list(view_categories())[:3]
    topics = list(view_topics(page=1, page_size=3))

    return templates.TemplateResponse("home.html", {"request": request, "categories": categories, "topics": topics})


app.mount("/static", StaticFiles(directory="static"), name="static")
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000)

