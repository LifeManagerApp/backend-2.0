from schemas.user import UserAuthRequest, UserAuthResponse
from utils.jwt import JWT
from crud.user_crud import UserCRUD


class AuthService:
    def __init__(self):
        self.user_crud = UserCRUD()
        self.jwt = JWT()

    async def auth(self, user: UserAuthRequest) -> UserAuthResponse | Exception:
        current_user = await self.user_crud.get_user(user=user)
        if current_user is None:
            return Exception("The user with such parameters was not found")

        access_token = await self.jwt.create_jwt_token(data={"sub": current_user.login})

        return UserAuthResponse(id=current_user.id, login=current_user.login, access_token=access_token)
