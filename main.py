from fastapi import FastAPI
from routers.router_users import users_router

app = FastAPI()

app.include_router(users_router)
