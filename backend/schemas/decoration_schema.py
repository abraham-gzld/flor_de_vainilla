from pydantic import BaseModel


class decorationCreate(BaseModel):

    name: str
    price_extra: float = 0


class decorationResponse(BaseModel):

    decoration_id: int
    name: str
    price_extra: float

    class Config:

        from_attributes = True