from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class quotationCreate(BaseModel):

    customer_id: int

    subtotal: float = 0
    total: float = 0
    status: str = "pending"
    note: Optional[str] = None


class quotationResponse(BaseModel):

    quotation_id: int
    customer_id: int

    quotation_date: datetime
    subtotal: float
    total: float

    status: str
    note: Optional[str]

    class Config:

        from_attributes = True