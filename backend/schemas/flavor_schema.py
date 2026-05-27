from pydantic import BaseModel


class flavorCreate(BaseModel):

    name: str
    price_extra: float = 0


class flavorResponse(BaseModel):

    flavor_id: int
    name: str
    price_extra: float

    class Config:

        from_attributes = True