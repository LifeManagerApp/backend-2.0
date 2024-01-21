from fastapi import APIRouter
from fastapi.exceptions import HTTPException

from schemas.user import UserAuthRequest, UserAuthResponse
from services.auth_service import AuthService

categories_router = APIRouter(prefix='/categories')

categories_router.tags = ["Categories"]

#put, patch, delete, get


@categories_router.get("/{user_id}", response_model=UserAuthResponse)
async def users_categories(user: UserAuthRequest):
    try:
        new_user = await auth_service.auth(user)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return new_user
