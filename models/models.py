from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, UUID, text, Date, Float
from sqlalchemy.orm import relationship
from .base import Base
import uuid
from datetime import datetime


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


class History(Base):
    __tablename__ = "history"

    id = Column(Integer, primary_key=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    users_category_id = Column(Integer, ForeignKey('user_categories.id', ondelete='CASCADE'), nullable=False)
    amount = Column(Float, nullable=False)
    comment = Column(String, nullable=True, default=None)
    transactions_type = Column(Boolean, nullable=False, default=True)  # Income - True, Expense - False
    date = Column(Date, default=datetime.now().date())

    user = relationship('User')
    user_categories = relationship('UsersCategory')
