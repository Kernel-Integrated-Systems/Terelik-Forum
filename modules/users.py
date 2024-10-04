from pydantic import BaseModel


class User(BaseModel):
    id: int | None = None
    username: str
    email: str
    password: str
    role: str | None = None
    is_active: bool


class UserRegistrationRequest(BaseModel):
    username: str
    email: str
    password: str


class UserLoginRequest(BaseModel):
    email: str
    password: str
