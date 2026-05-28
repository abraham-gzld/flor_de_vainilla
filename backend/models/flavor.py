from sqlalchemy import Column, Integer, String, DECIMAL

from backend.config.connection import Base

class Flavor(Base):

    __tablename__ = "flavor"

    flavor_id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    name = Column(
        String(50),
        nullable=False,
        unique=True
    )

    price_extra = Column(
        DECIMAL(10,2),
        default=0
    )
