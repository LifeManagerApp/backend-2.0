from fastapi_sqlalchemy import db


class DBOperations:
    async def db_write(self, entity):
        db.session.add(entity)
        db.session.commit()

    async def db_write_list(self, entity):
        db.session.add_all(entity)
        db.session.commit()

    async def db_delete(self, entity):
        db.session.delete(entity)
        db.session.commit()
