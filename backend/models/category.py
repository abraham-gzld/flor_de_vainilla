from sqlalchemy import Column, Integer, String, Text, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from backend.config.connection import Base

class Category(Base):
    __tablename__ = "category"

    category_id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String(100), nullable=False)

    products = relationship(
        "Product",
        back_populates="category"
    )