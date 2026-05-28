from pydantic import BaseModel

class SizeCreate(BaseModel):

    name: str
    price_extra: float = 0


class SizeResponse(BaseModel):

    size_id: int
    name: str
    price_extra: float

    class Config:

        from_attributes = True