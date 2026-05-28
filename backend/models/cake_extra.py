from sqlalchemy import Column, Integer, ForeignKey

from sqlalchemy.orm import relationship

from backend.config.connection import Base

class CakeExtra(Base):
    __tablename__ = "cake_extra"

    cake_id = Column(
        Integer,
        ForeignKey("custom_cake.cake_id"),
        primary_key=True
    )

    extra_id = Column(
        Integer,
        ForeignKey("extra.extra_id"),
        primary_key=True
    )

    cake = relationship(
        "CustomCake",
        back_populates="extras"
    )

    extra = relationship(
        "Extra"
    )