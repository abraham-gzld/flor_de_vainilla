from sqlalchemy import Column, Integer, DECIMAL, Text, ForeignKey, Enum, TIMESTAMP

from sqlalchemy.sql import func 
from sqlalchemy.orm import relationship

from backend.config.connection import Base

class Quotation(Base):
    __tablename__="quotation"

    quotation_id = Column(Integer, primary_key=True, autoincrement=True)

    customer_id = Column(
        Integer,
        ForeignKey("customer.customer_id"),
        nullable=False
    )

    quotation_date  = Column(
        TIMESTAMP,
        server_default=func.now()
    )

    subtotal = Column(
        DECIMAL(10,2),
        nullable=False,
        default=0
    )

    total = Column(
        DECIMAL(10,2),
        nullable=False,
        default=0
    )

    status = Column(
        Enum("pending", "approved", "canceled"),
        default="pending"
    )

    note = Column(Text)

    customer = relationship(
        "Customer",
        back_populates="quotations"
    )

    details = relationship(
        "DetailQuotation",
        back_populates="quotation"
    )