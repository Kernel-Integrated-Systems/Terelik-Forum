from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer

from routers.router_messages import messages_router
from routers.router_users import users_router


SECRET_KEY = 'add secret key'
ALGORITHM = 'HS256'
DEFAULT_TOKEN_EXPIRY_TIME = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()

app.include_router(users_router)
app.include_router(messages_router)



