from pydantic import BaseModel


class User(BaseModel):
    id: int | None = None
    username: str
    email: str
    role: int | None = None
    is_active: bool

    @classmethod
    def from_query_result(cls, id, username, email, role, is_active):
        return cls(
            id=id,
            username=username,
            email=email,
            role=role,
            is_active=is_active
        )

class UserRegistrationRequest(BaseModel):
    username: str
    email: str
    password: str


class UserLoginRequest(BaseModel):
    email: str
    password: str
