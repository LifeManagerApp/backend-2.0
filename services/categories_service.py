from typing import Type

from crud.categories_crud import CategoriesCrud
from crud.user_crud import UserCRUD
from models.models import Categories
from schemas.categories import AddUserCategory, UsersCategoriesResponse, ChangeUserCategory


class CategoriesService:
    def __init__(self):
        self.categories_crud = CategoriesCrud()
        self.user_crud = UserCRUD()

    async def get_user_categories(self, login: str) -> list[Type[Categories]]:
        user = await self.user_crud.get_user(login=login)
        categories = await self.categories_crud.get_categories(user_id=user.id)
        return categories

    async def update_user_category(
            self,
            login: str,
            change_category: ChangeUserCategory
    ) -> ChangeUserCategory | Exception:

        user = await self.user_crud.get_user(login=login)
        category = await self.categories_crud.update_user_category(user_id=user.id, change_category=change_category)
        if type(category) is not Exception:
            return change_category

        return category

    async def add_user_category(
            self,
            login: str,
            new_category: AddUserCategory
    ) -> UsersCategoriesResponse | Exception:

        user = await self.user_crud.get_user(login=login)
        category = await self.categories_crud.add_user_category(user_id=user.id, new_category=new_category)

        if type(category) is not Exception:
            return UsersCategoriesResponse(
                id=category[1].id,
                category_name=category[0].category_name,
                color=category[0].color
            )

        return category

    async def delete_user_category(self, login: str, category_id: int) -> int | Exception:
        user = await self.user_crud.get_user(login=login)

        if user is None:
            return Exception('Incorrect user')

        category = await self.categories_crud.delete_category(category_id=category_id)
        if category is None:
            return Exception('Incorrect category id')

        return category_id
