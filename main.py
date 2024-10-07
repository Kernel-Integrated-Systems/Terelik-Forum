from fastapi import FastAPI

from routers.router_replies import replies_router, votes_router
from routers.router_topics import topics_router
from routers.router_users import users_router

app = FastAPI()

@app.get('/')
def get_main(sort: str | None):
    pass
    return sort


app.include_router(replies_router)
app.include_router(votes_router)
app.include_router(topics_router)
app.include_router(users_router)