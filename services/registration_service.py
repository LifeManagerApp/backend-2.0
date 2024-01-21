from schemas.user import UserCreateRequest, UserAuthResponse
from services.user_service import UserService
from utils.jwt import JWT


class RegistrationService(UserService, JWT):
    async def registration(self, user: UserCreateRequest) -> UserAuthResponse:
        try:
            new_user = await self.create_user(user=user)
        except Exception as e:
           raise e

        access_token = await self.create_jwt_token(data={"sub": new_user.login})

        return UserAuthResponse(id=new_user.id, login=new_user.login, access_token=access_token)
