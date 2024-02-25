from fastapi import APIRouter, Depends

from schemas.history import NewRecord, NewRecordResponse, UserRecord, ChangeUserRecord
from services.history_service import HistoryService

from utils.jwt import JWT

history_router = APIRouter(prefix='/history')

history_router.tags = ["History"]

history_service = HistoryService()


@history_router.put("/", response_model=NewRecordResponse)
async def add_history(new_record: NewRecord, current_user=Depends(JWT.get_current_user)):
    new_record_id = await history_service.set_record(login=current_user, new_record=new_record)
    return NewRecordResponse(record_id=new_record_id)


@history_router.get("/", response_model=list[UserRecord])
async def get_all_history(current_user=Depends(JWT.get_current_user)):
    all_records = await history_service.get_all_records(login=current_user)
    return all_records


@history_router.patch("/", response_model=UserRecord)
async def refactor_history(change_record: ChangeUserRecord, current_user=Depends(JWT.get_current_user)):
    updated_record = await history_service.update_record(login=current_user, change_record=change_record)
    return updated_record


@history_router.delete("/", response_model=NewRecordResponse)
async def delete_record(record_id: int, current_user=Depends(JWT.get_current_user)):
    deleted_record_id = await history_service.delete_record(record_id=record_id)
    return NewRecordResponse(record_id=deleted_record_id)
