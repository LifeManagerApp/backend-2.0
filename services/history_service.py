from typing import Type

from crud.history_crud import HistoryCrud
from crud.user_crud import UserCRUD
from schemas.categories import UsersCategoriesResponse
from schemas.history import NewRecord, UserRecord, ChangeUserRecord


class HistoryService:
    def __init__(self):
        self.history_crud = HistoryCrud()
        self.user_crud = UserCRUD()

    async def set_record(self, login: str, new_record: NewRecord) -> int:
        user = await self.user_crud.get_user(login=login)
        new_record_id = await self.history_crud.set_new_record(user_id=user.id, new_record=new_record)

        return new_record_id

    async def get_all_records(self, login: str) -> list[UserRecord]:
        user = await self.user_crud.get_user(login=login)
        query_result = await self.history_crud.get_all_records(user_id=user.id)

        all_records = []

        for record in query_result:
            all_records.append(
                UserRecord(
                    id=record.id,
                    category=UsersCategoriesResponse
                    (
                        id=record.user_category_id,
                        category_name=record.category_name,
                        color=record.category_color
                    ),
                    amount=record.amount,
                    comment=record.comment,
                    transactions_type=record.transactions_type,
                    date=record.date
                )
            )

        return all_records

    async def update_record(self, login: str, change_record: ChangeUserRecord) -> UserRecord:
        user = await self.user_crud.get_user(login=login)
        record = await self.history_crud.update_record(user_id=user.id, change_record=change_record)
        print(record)

        updated_record = UserRecord(
            id=record.id,
            category=UsersCategoriesResponse
                (
                id=record.user_category_id,
                category_name=record.category_name,
                color=record.category_color
            ),
            amount=record.amount,
            comment=record.comment,
            transactions_type=record.transactions_type,
            date=record.date
        )

        return updated_record

    async def delete_record(self, record_id: int) -> int:
        await self.history_crud.delete_record(record_id=record_id)
        return record_id
