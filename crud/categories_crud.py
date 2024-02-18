from typing import Type

from fastapi_sqlalchemy import db
from sqlalchemy.orm import aliased

from schemas.categories import AddUserCategory, ChangeUserCategory
from .db_operations import DBOperations
from models.models import Categories, UsersCategory
from pydantic import UUID4


class CategoriesCrud(DBOperations):
    async def _get_default_categories(self) -> list[Type[Categories]]:
        default_categories = db.session.query(Categories).filter(
            Categories.is_default == True
        ).all()

        return default_categories

    async def _get_user_categories(self, user_id: UUID4) -> list[Type[Categories]]:
        user_categories = db.session.query(
            aliased(Categories, name='category'),
            UsersCategory.id.label('users_category_id')
        ).join(UsersCategory).filter(
            UsersCategory.user_id == user_id
        ).all()
        return user_categories

    async def _check_common_category_existence(self, category_name: str, color: str) -> Type[Categories] | None:
        category = db.session.query(Categories).filter(
            Categories.category_name == category_name,
            Categories.color == color
        ).first()

        return category

    async def _check_user_category_existence(
            self,
            common_category_id: int,
            user_id: UUID4
    ) -> Type[UsersCategory] | None:
        category = db.session.query(UsersCategory).filter(
            UsersCategory.user_id == user_id,
            UsersCategory.category_id == common_category_id
        ).first()

        return category

    async def get_categories(
            self,
            is_default: bool = None,
            user_id: UUID4 = None
    ) -> list[Type[Categories]]:
        categories = None

        if is_default:
            categories = await self._get_default_categories()

        if user_id is not None:
            categories = await self._get_user_categories(user_id=user_id)

        return categories

    async def set_default_categories(self, user_id: UUID4):
        categories = await self.get_categories(is_default=True)

        users_default_categories = []

        for category in categories:
            users_default_categories.append(
                UsersCategory(
                    user_id=user_id,
                    category_id=category.id
                )
            )

        await self.db_write_list(users_default_categories)

    async def _add_common_category(self, category_name: str, color: str) -> Categories:
        new_common_category = Categories(category_name=category_name, color=color)
        await self.db_write(new_common_category)
        return new_common_category

    async def _add_user_category(self, common_category_id: int, user_id: UUID4) -> UsersCategory:
        new_user_category = UsersCategory(
            category_id=common_category_id,
            user_id=user_id
        )
        await self.db_write(new_user_category)
        return new_user_category

    async def add_user_category(
            self,
            new_category: AddUserCategory,
            user_id: UUID4
    ) -> tuple[Categories, UsersCategory] | Exception:

        common_category = await self._check_common_category_existence(
            category_name=new_category.category_name,
            color=new_category.color
        )

        if common_category is not None:
            user_category = await self._check_user_category_existence(
                common_category_id=common_category.id,
                user_id=user_id
            )
            if user_category is not None:
                return Exception('This user already has such a category')
        else:
            common_category = await self._add_common_category(
                category_name=new_category.category_name,
                color=new_category.color
            )

        new_user_category = await self._add_user_category(
            common_category_id=common_category.id,
            user_id=user_id
        )

        return common_category, new_user_category

    async def _get_user_category_by_id(self, user_category_id: int) -> Type[UsersCategory] | None:
        category = db.session.query(UsersCategory).filter(
            UsersCategory.id == user_category_id
        ).first()

        return category

    async def update_user_category(
            self,
            change_category: ChangeUserCategory,
            user_id: UUID4
    ) -> Type[UsersCategory] | Exception:

        current_category = await self._get_user_category_by_id(user_category_id=change_category.id)

        common_category = await self._check_common_category_existence(
            category_name=change_category.category_name,
            color=change_category.color
        )

        if common_category is not None:
            user_category = await self._check_user_category_existence(
                common_category_id=common_category.id,
                user_id=user_id
            )

            if user_category is not None:
                return Exception('You are trying to replace a category with an existing one')
        else:
            common_category = await self._add_common_category(
                category_name=change_category.category_name,
                color=change_category.color
            )

        current_category.category_id = common_category.id
        db.session.commit()

        return current_category

    async def delete_category(self, category_id: int) -> Type[UsersCategory]:
        category = await self._get_user_category_by_id(user_category_id=category_id)

        await self.db_delete(category)

        return category
