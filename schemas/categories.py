from pydantic import BaseModel


class UsersCategoriesResponse(BaseModel):
    id: int
    category_name: str
    color: str


class AddUserCategory(BaseModel):
    category_name: str
    color: str


class ChangeUserCategory(BaseModel):
    id: int
    category_name: str = None
    color: str = None
