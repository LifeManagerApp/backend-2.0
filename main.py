import os
from dotenv import load_dotenv
from common.logger import logger

if os.path.exists('.env'):
    load_dotenv('.env')
    logger.info('.env loaded successful')
else:
    logger.error('.env file is not detected')


import uvicorn
from fastapi import FastAPI
from controllers.auth_controller import auth_router
from controllers.registration_controller import regist_router
from controllers.categories_controller import categories_router
from models.base import Base
from fastapi_sqlalchemy import DBSessionMiddleware
from settings.db_settings import DBSettings


app = FastAPI(openapi_prefix="/api/v1")
app.add_middleware(DBSessionMiddleware, db_url=f'postgresql+psycopg2://{DBSettings.CONNECTION_DATA}')

app.include_router(auth_router)
app.include_router(regist_router)
app.include_router(categories_router)


if __name__ == "__main__":
    Base.metadata.create_all(bind=DBSettings.engine)
    uvicorn.run(app, port=9000)
