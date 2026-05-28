from pydantic import BaseModel
from typing import Optional


class customCakeBase(BaseModel):
    detail_id: int
    size_id: int
    flavor_id: int
    filling_id: int
    decoration_id: int
    servings: Optional[int] = None
    base_price: float
    final_price: float
    description: Optional[str] = None


class customCakeCreate(customCakeBase):
    pass


class customCakeResponse(customCakeBase):
    cake_id: int

    model_config = {
        "from_attributes": True
    }