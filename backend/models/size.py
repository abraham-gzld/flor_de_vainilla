from sqlalchemy import Column, Integer, String, DECIMAL
from backend.config.connection import Base

class Size(Base):

    __tablename__ = "size"

    size_id = Column(Integer, primary_key=True, index=True)

    name = Column(String(50), nullable=False, unique=True)

    price_extra = Column(DECIMAL(10,2), default=0)