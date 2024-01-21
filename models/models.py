from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, UUID, text
from sqlalchemy.orm import relationship
from .base import Base
import uuid


class User(Base):
    __tablename__ = "user"

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"), index=True, default=uuid.uuid4)
    login = Column(String, nullable=True, unique=True)
    password = Column(String, nullable=True)
    email = Column(String, nullable=True)
    tg_id = Column(String, nullable=True)


class Categories(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    category_name = Column(String, nullable=False)
    color = Column(String, nullable=False)
    is_default = Column(Boolean, nullable=False, default=False)


class UsersCategory(Base):
    __tablename__ = "user_categories"

    id = Column(Integer, primary_key=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id', ondelete='CASCADE'), nullable=False)

    user = relationship('User')
    categories = relationship('Categories')
