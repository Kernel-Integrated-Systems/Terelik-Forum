from fastapi import FastAPI
from routers.router_topics import topics_router
from routers.router_categories import categories_router
app = FastAPI()

app.include_router(topics_router)
app.include_router(categories_router)
