from fastapi import APIRouter
from fastapi.exceptions import HTTPException

from schemas.user import UserCreateRequest, UserAuthResponse
from services.registration_service import RegistrationService

regist_router = APIRouter(prefix='/registration')

regist_router.tags = ["Registration"]

registration_service = RegistrationService()


@regist_router.post("/", response_model=UserAuthResponse)
async def registration(user: UserCreateRequest):
    new_user = await registration_service.registration(user)
    if type(new_user) is Exception:
        raise HTTPException(status_code=400, detail=str(new_user))

    return new_user

