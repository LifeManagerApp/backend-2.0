from sqlalchemy import Column, String, UUID, text
from models.base import Base
import uuid


class UserModel(Base):
    __tablename__ = "user"

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"), index=True, default=uuid.uuid4)
    login = Column(String, nullable=True, unique=True)
    password = Column(String, nullable=True)
    email = Column(String, nullable=True)
    tg_id = Column(String, nullable=True)
