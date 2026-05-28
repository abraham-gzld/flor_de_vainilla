from pydantic import BaseModel, Field
from typing import Optional


# CREATE
class detailQuotationCreate(BaseModel):

    quotation_id: int

    product_id: Optional[int] = None

    product_type: str

    quantity: int = Field(gt=0)

    unit_price: float

    subtotal: float

    comment: Optional[str] = None


# UPDATE QUANTITY
class detailQuantityUpdate(BaseModel):

    quantity: int = Field(gt=0)


# RESPONSE
class detailQuotationResponse(BaseModel):

    detail_id: int

    quotation_id: int

    product_id: Optional[int] = None

    product_type: str

    quantity: int

    unit_price: float

    subtotal: float

    comment: Optional[str] = None

    model_config = {
        "from_attributes": True
    }