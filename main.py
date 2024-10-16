from fastapi import FastAPI

from routers.router_categories import categories_router
from routers.router_topics import topics_router
from routers.router_replies import replies_router, votes_router, best_reply_router
from routers.router_messages import messages_router
from routers.router_users import users_router
from data.database import database_init


database_init()

app = FastAPI()

app.include_router(replies_router)
app.include_router(votes_router)
app.include_router(topics_router)
app.include_router(users_router)
app.include_router(messages_router)
app.include_router(best_reply_router)
app.include_router(categories_router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000)