from pydantic import BaseModel

class detailQuotationCreate(BaseModel):

    quotation_id: int
    product_id: int | None = None

    product_type: str

    quantity: int = 1

    unit_price: float

    subtotal: float

    comment: str | None = None


class detailQuotationResponse(BaseModel):

    detail_id: int

    quotation_id: int
    product_id: int | None = None

    product_type: str

    quantity: int

    unit_price: float

    subtotal: float

    comment: str | None = None

    class Config:
        from_attributes = True