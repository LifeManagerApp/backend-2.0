from schemas.user import UserCreateRequest, UserAuthResponse
from utils.jwt import JWT
from crud.user_crud import UserCRUD
from crud.categories_crud import CategoriesCrud


class RegistrationService:
    def __init__(self):
        self.user_crud = UserCRUD()
        self.jwt = JWT()
        self.categories_crud = CategoriesCrud()

    async def registration(self, user: UserCreateRequest) -> UserAuthResponse | Exception:
        new_user = await self.user_crud.create(user=user)

        if type(new_user) is Exception:
            return new_user

        await self.categories_crud.set_default_categories(new_user.id)

        access_token = await self.jwt.create_jwt_token(data={"sub": new_user.login})

        return UserAuthResponse(id=new_user.id, login=new_user.login, access_token=access_token)
