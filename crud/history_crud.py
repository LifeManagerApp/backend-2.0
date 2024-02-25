from typing import Type

from pydantic import UUID4
from fastapi_sqlalchemy import db

from crud.db_operations import DBOperations

from models.models import History, UsersCategory, Categories
from schemas.history import NewRecord, ChangeUserRecord


class HistoryCrud(DBOperations):
    async def set_new_record(self, new_record: NewRecord, user_id: UUID4) -> int:
        record = History(
            user_id=user_id,
            users_category_id=new_record.users_category_id,
            amount=new_record.amount,
            comment=new_record.comment,
            transactions_type=new_record.transactions_type,
            date=new_record.date
        )
        await self.db_write(record)

        return record.id

    async def get_all_records(self, user_id: UUID4):
        all_records = (db.session.query(
            History.id.label('id'),
            History.amount.label('amount'),
            History.comment.label('comment'),
            History.transactions_type.label('transactions_type'),
            History.date.label('date'),
            UsersCategory.id.label('user_category_id'),
            Categories.color.label('category_color'),
            Categories.category_name.label('category_name')
        )
                       .join(UsersCategory, History.users_category_id == UsersCategory.id)
                       .join(Categories, UsersCategory.category_id == Categories.id)
                       .filter(History.user_id == user_id)
                       .all())

        return all_records

    async def _get_record(self, record_id: int) -> Type[History] | None:
        record = db.session.query(History).filter(History.id == record_id).first()
        return record

    async def update_record(self, user_id: UUID4, change_record: ChangeUserRecord):
        record = await self._get_record(record_id=change_record.id)

        if change_record.amount is not None:
            record.amount = change_record.amount
        if change_record.comment is not None:
            record.comment = change_record.comment

        db.session.commit()

        updated_record = (db.session.query(
            History.id.label('id'),
            History.amount.label('amount'),
            History.comment.label('comment'),
            History.transactions_type.label('transactions_type'),
            History.date.label('date'),
            UsersCategory.id.label('user_category_id'),
            Categories.color.label('category_color'),
            Categories.category_name.label('category_name')
        )
                       .join(UsersCategory, History.users_category_id == UsersCategory.id)
                       .join(Categories, UsersCategory.category_id == Categories.id)
                       .filter(History.user_id == user_id, History.id == change_record.id)
                       .first())

        return updated_record

    async def delete_record(self, record_id: int):
        record = await self._get_record(record_id=record_id)

        await self.db_delete(record)
