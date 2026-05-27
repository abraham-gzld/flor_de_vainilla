from pydantic import BaseModel


class fillingCreate(BaseModel):

    name: str
    price_extra: float = 0


class fillingResponse(BaseModel):

    filling_id: int
    name: str
    price_extra: float

    class Config:

        from_attributes = True