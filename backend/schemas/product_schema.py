from pydantic import BaseModel

class productCreate(BaseModel):
    category_id: int
    name: str
    description: str | None = None
    base_price: float
    image_url: str | None = None
    active: bool=True

class productResponse(BaseModel):

    product_id: int
    category_id: int
    name: str
    description: str | None = None
    base_price: float
    image_url: str | None = None
    active: bool

    class Config:

        from_attributes = True
