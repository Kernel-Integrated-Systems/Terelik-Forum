from pydantic import BaseModel
from datetime import datetime

class User(BaseModel):
    user_id: int
    username: str
    email: str
    password: str
    role: int
    is_active: bool
    created_at: datetime

    @classmethod
    def get_user(cls, user_id: int, username: str, email, password, role, is_active, created_at):
        return cls(
            user_id=user_id,
            username=username,
            email=email,
            password=password,
            role=role,
            is_active=is_active,
            created_at=created_at
        )

class UserRegistrationRequest(BaseModel):
    username: str
    email: str
    password: str


class UserLoginRequest(BaseModel):
    email: str
    password: str
