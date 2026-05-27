from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import DECIMAL

from backend.config.connection import Base


class Extra(Base):

    __tablename__ = "extra"

    extra_id = Column(
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