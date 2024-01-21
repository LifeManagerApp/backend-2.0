from schemas.user import UserAuthRequest, UserAuthResponse
from services.user_service import UserService
from utils.jwt import JWT


class AuthService(UserService, JWT):
    async def auth(self, user: UserAuthRequest) -> UserAuthResponse:
        try:
            current_user = await self.get_user(user=user)
        except Exception as e:
           raise e

        access_token = await self.create_jwt_token(data={"sub": current_user.login})

        return UserAuthResponse(id=current_user.id, login=current_user.login, access_token=access_token)
