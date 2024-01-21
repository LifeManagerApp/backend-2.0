from pydantic import BaseModel


class UsersCategoriesResponse(BaseModel):
    id: int
    category_name: str
    color: str
