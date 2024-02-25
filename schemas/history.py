from pydantic import BaseModel
from datetime import date

from schemas.categories import UsersCategoriesResponse


class NewRecord(BaseModel):
    users_category_id: int
    amount: float
    comment: str = None
    transactions_type: bool
    date: date


class NewRecordResponse(BaseModel):
    record_id: int


class UserRecord(BaseModel):
    id: int
    category: UsersCategoriesResponse
    amount: float
    comment: str = None
    transactions_type: bool
    date: date


class ChangeUserRecord(BaseModel):
    id: int
    amount: float = None
    comment: str = None
