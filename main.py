from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routers.router_categories import categories_router as api_categories_router
from routers.router_topics import topics_router as api_topics_router
from routers.router_replies import replies_router as api_replies_router
from routers.router_messages import messages_router as api_messages_router
from routers.router_users import users_router as api_users_router
from data.database import database_init
from web_routers.router_home import index_router as web_index_router
from web_routers.router_users import users_router as web_users_router
from web_routers.router_categories import categories_router as web_categories_router

database_init()

app = FastAPI()
# Mount static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(api_replies_router)
app.include_router(api_topics_router)
app.include_router(api_users_router)
app.include_router(api_messages_router)
app.include_router(api_categories_router)

app.include_router(web_index_router)
app.include_router(web_users_router)
app.include_router(web_categories_router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000)