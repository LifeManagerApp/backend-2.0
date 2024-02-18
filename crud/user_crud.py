from typing import Type

from fastapi_sqlalchemy import db

from schemas.user import UserAuthRequest, UserCreateRequest
from models.models import User
from .db_operations import DBOperations


class UserCRUD(DBOperations):
    async def create(self, user: UserCreateRequest) -> Type[User] | Exception:
        db_user = User(**user.dict())

        exist_user = await self.get_user(login=user.login)

        if exist_user is not None:
            return Exception("User with this login already exists")

        await self.db_write(db_user)
        return db_user

    async def update(self):
        pass

    async def delete(self):
        pass

    async def _get_user_by_login(self, login: str) -> Type[User] | None:
        current_user = db.session.query(User).filter(
            User.login == login
        ).first()

        return current_user

    async def _get_user_by_login_and_password(self, user: UserAuthRequest) -> Type[User] | None:
        current_user = db.session.query(User).filter(
            User.login == user.login,
            User.password == user.password
        ).first()

        return current_user

    async def get_user(
            self,
            user: UserAuthRequest = None,
            login: str = None
    ) -> Type[User] | None:
        current_user = None

        if user is not None:
            current_user = await self._get_user_by_login_and_password(user)

        if login is not None:
            current_user = await self._get_user_by_login(login)

        return current_user
