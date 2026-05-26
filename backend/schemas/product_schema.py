from pydantic import BaseModel

class productCreate(BaseModel):
    category_id: int
    name: str
    description: str | None = None
    base_price: float
    active: bool=True

class productResponse(BaseModel):

    product_id: int
    category_id: int
    name: str
    description: str | None = None
    base_price: float
    active: bool

    class Config:

        from_attributes = True