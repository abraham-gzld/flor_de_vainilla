from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from backend.config.connection import Base

class Category(Base):
    __tablename__ = "category"

    category_id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String(50), nullable=False, unique=True)

    products = relationship(
        "Product",
        back_populates="category"
    )
