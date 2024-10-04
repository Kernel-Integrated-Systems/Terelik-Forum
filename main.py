from fastapi import FastAPI
from routers.router_topics import topics_router
app = FastAPI()

app.include_router(topics_router)