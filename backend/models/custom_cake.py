from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy import DECIMAL, Text

from sqlalchemy.orm import relationship

from backend.config.connection import Base

from backend.models.size import Size
from backend.models.flavor import Flavor
from backend.models.filling import Filling
from backend.models.decoration import Decoration

class CustomCake(Base):
    __tablename__ = "custom_cake"

    cake_id = Column(Integer, primary_key=True, autoincrement=True)

    detail_id = Column(
        Integer,
        ForeignKey("detail_quotation.detail_id"),
        nullable=False
    )

    size_id = Column(
        Integer,
        ForeignKey("size.size_id"),
        nullable=False
    )

    flavor_id = Column(
        Integer,
        ForeignKey("flavor.flavor_id"),
        nullable=False
    )

    filling_id = Column(
        Integer,
        ForeignKey("filling.filling_id"),
        nullable=False
    )

    decoration_id = Column(
        Integer,
        ForeignKey("decoration.decoration_id"),
        nullable=False
    )

    servings = Column(Integer)

    base_price = Column(DECIMAL(10,2), nullable=False)

    final_price = Column(DECIMAL(10,2), nullable=False)

    description = Column(Text)

    detail = relationship(
        "DetailQuotation",
        back_populates="custom_cake"
    )

    size = relationship("Size")
    flavor = relationship("Flavor")
    filling = relationship("Filling")
    decoration = relationship("Decoration")

    extras = relationship(
        "CakeExtra",
        back_populates="cake"
    )