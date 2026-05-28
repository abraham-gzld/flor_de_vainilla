from sqlalchemy import Column, Integer, String, Text, TIMESTAMP
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from backend.config.connection import Base

class Customer(Base):
    __tablename__ = "customer"

    customer_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=False)
    address = Column(Text)

    register_date = Column(
        TIMESTAMP,
        server_default=func.now()
    )
    quotations = relationship(
    "Quotation",
    back_populates="customer"
)