from typing import List
from fastapi import APIRouter
from fastapi.exceptions import HTTPException

from schemas.categories import UsersCategoriesResponse


from services.auth_service import AuthService

categories_router = APIRouter(prefix='/categories')

categories_router.tags = ["Categories"]

#put, patch, delete, get


@categories_router.get("/{user_id}")
async def users_categories(user_id: int):

    return {'user_id': user_id}


@categories_router.patch("/{user_id}/{category_id}")
async def update_users_categories(user_id: int):
    pass


@categories_router.delete("/{user_id}/{category_id}")
async def delete_users_categories(user_id: int):
    pass


@categories_router.put("/{user_id}/{category_id}")
async def add_users_categories(user_id: int):
    pass
