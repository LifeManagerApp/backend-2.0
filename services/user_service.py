from typing import Type

from models.models import User
from schemas.user import UserAuthRequest, UserCreateRequest
from fastapi_sqlalchemy import db


class UserService:
    async def __check_user_existence(self, login: str) -> bool:
        exist_user = db.session.query(User).filter(User.login == login).first()
        if exist_user is None:
            return False

        return True

    async def create_user(self, user: UserCreateRequest) -> User:
        db_user = User(**user.dict())

        exist_user = await self.__check_user_existence(user.login)

        if exist_user:
            raise Exception("User with this login already exists")

        db.session.add(db_user)
        db.session.commit()
        return db_user

    async def get_user(self, user: UserAuthRequest) -> Type[User]:
        current_user = db.session.query(User).filter(
            User.login == user.login,
            User.password == user.password
        ).first()

        if current_user is None:
            raise Exception("Login or password is incorrect")

        return current_user
