from pydantic import BaseModel


class extraCreate(BaseModel):

    name: str
    price_extra: float = 0


class extraResponse(BaseModel):

    extra_id: int
    name: str
    price_extra: float

    class Config:

        from_attributes = True