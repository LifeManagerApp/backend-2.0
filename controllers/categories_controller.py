from typing import List
from fastapi import APIRouter
from fastapi.exceptions import HTTPException

from schemas.categories import UsersCategoriesResponse


from services.auth_service import AuthService

categories_router = APIRouter(prefix='/categories')

categories_router.tags = ["Categories"]

#put, patch, delete, get


@categories_router.get("/{user_id}", response_model=List[UsersCategoriesResponse])
async def users_categories(user_id: int):
    try:
        new_user = await auth_service.auth(user)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return new_user
