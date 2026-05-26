from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy import DECIMAL
from sqlalchemy import Boolean
from sqlalchemy import ForeignKey

from sqlalchemy.orm import relationship

from backend.config.connection import Base

class Product(Base):
    __tablename__ = "product"

    product_id = Column(Integer, primary_key=True, autoincrement=True)
    category_id = Column(Integer, ForeignKey("category.category_id"), nullable=False)

    name = Column(String(100), nullable=False)
    description = Column(Text)
    base_price = Column(DECIMAL(10,2), nullable=False)

    active = Column(Boolean, default=True)
    category = relationship("Category", back_populates="products")
