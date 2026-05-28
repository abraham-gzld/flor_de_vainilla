from pydantic import BaseModel
from typing import Optional


class customCakeCreate(BaseModel):
    detail_id: int
    size_id: int
    flavor_id: int
    filling_id: int
    decoration_id: int
    servings: Optional[int] = None
    description: Optional[str] = None


class customCakeResponse(customCakeCreate):
    cake_id: int
    base_price: float
    final_price: float

    model_config = {
        "from_attributes": True
    }
