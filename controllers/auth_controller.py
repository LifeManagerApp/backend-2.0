from fastapi import APIRouter
from fastapi.exceptions import HTTPException

from schemas.user import UserAuthRequest, UserAuthResponse
from services.auth_service import AuthService

auth_router = APIRouter(prefix='/auth')

auth_router.tags = ["Authentication"]

auth_service = AuthService()


@auth_router.post("/", response_model=UserAuthResponse)
async def auth(user: UserAuthRequest):
    current_user = await auth_service.auth(user)

    if type(current_user) is Exception:
        raise HTTPException(status_code=400, detail=str(current_user))

    return current_user
