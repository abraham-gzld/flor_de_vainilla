from sqlalchemy import Column, Integer, String, DECIMAL, Text, TIMESTAMP

from backend.config.connection import Base

from backend.config.connection import Base


class Flavor(Base):

    __tablename__ = "flavor"

    flavor_id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    name = Column(
        String(100),
        nullable=False
    )

    price_extra = Column(
        DECIMAL(10,2),
        default=0
    )