from fastapi import APIRouter
from fastapi.exceptions import HTTPException

from schemas.user import UserCreateRequest, UserAuthResponse
from services.registration_service import RegistrationService

regist_router = APIRouter(prefix='/registration')

regist_router.tags = ["Registration"]

registration_service = RegistrationService()


@regist_router.post("/", response_model=UserAuthResponse)
async def registration(user: UserCreateRequest):
    try:
        new_user = await registration_service.registration(user)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return new_user

