from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import DECIMAL

from backend.config.connection import Base


class Decoration(Base):

    __tablename__ = "decoration"

    decoration_id = Column(
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
