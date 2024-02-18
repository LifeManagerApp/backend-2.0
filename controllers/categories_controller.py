from typing import List
from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException

from schemas.categories import UsersCategoriesResponse, AddUserCategory, ChangeUserCategory
from services.categories_service import CategoriesService

from utils.jwt import JWT


categories_router = APIRouter(prefix='/categories')

categories_router.tags = ["Categories"]

categories_service = CategoriesService()


@categories_router.get("/", response_model=List[UsersCategoriesResponse])
async def users_categories(current_user=Depends(JWT.get_current_user)):
    categories = await categories_service.get_user_categories(current_user)
    users_categories_response = []
    for category in categories:
        users_categories_response.append(
            UsersCategoriesResponse(
                id=category.users_category_id,
                category_name=category.category.category_name,
                color=category.category.color
            )
        )
    return users_categories_response


@categories_router.patch("/", response_model=ChangeUserCategory)
async def update_users_categories(change_category: ChangeUserCategory, current_user=Depends(JWT.get_current_user)):
    category = await categories_service.update_user_category(login=current_user, change_category=change_category)
    if type(category) is Exception:
        raise HTTPException(status_code=400, detail=str(category))
    return category


@categories_router.delete("/", response_model=int)
async def delete_users_categories(category_id: int, current_user=Depends(JWT.get_current_user)):
    category = await categories_service.delete_user_category(login=current_user, category_id=category_id)
    if type(category) is Exception:
        raise HTTPException(status_code=400, detail=str(category))
    return category


@categories_router.put("/", response_model=UsersCategoriesResponse)
async def add_users_categories(new_category: AddUserCategory, current_user=Depends(JWT.get_current_user)):
    category = await categories_service.add_user_category(login=current_user, new_category=new_category)
    if type(category) is Exception:
        raise HTTPException(status_code=400, detail=str(category))
    return category
