from pydantic import BaseModel, EmailStr, UUID4


class UserCreateRequest(BaseModel):
    email: EmailStr
    login: str
    password: str


class UserAuthResponse(BaseModel):
    id: UUID4
    login: str
    access_token: str


class UserAuthRequest(BaseModel):
    login: str
    password: str
