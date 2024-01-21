from sqlalchemy import Column, String, Integer, Boolean
from models.base import Base


class Categories(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    category_name = Column(String, nullable=False)
    color = Column(String, nullable=False)
    is_default = Column(Boolean, nullable=False, default=False)
