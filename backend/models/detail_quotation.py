from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy import DECIMAL, Text, Enum

from sqlalchemy.orm import relationship

from backend.config.connection import Base

class DetailQuotation(Base):
    __tablename__ = "detail_quotation"

    detail_id = Column(Integer, primary_key=True, autoincrement=True)

    quotation_id = Column(
        Integer,
        ForeignKey("quotation.quotation_id"),
        nullable=False
    )

    product_id = Column(
        Integer,
        ForeignKey("product.product_id"),
        nullable=True
    )

    product_type = Column(
        Enum(
            "simple_product",
            "custom_cake"
        ),
        nullable=False
    )

    quantity = Column(Integer, default=1)

    unit_price = Column(DECIMAL(10,2), nullable=False)

    subtotal = Column(DECIMAL(10,2), nullable=False)

    comment = Column(Text)

    quotation = relationship(
        "Quotation",
        back_populates="details"
    )

    product = relationship(
        "Product"
    )

    custom_cake = relationship(
        "CustomCake",
        back_populates="detail",
        uselist=False
    )