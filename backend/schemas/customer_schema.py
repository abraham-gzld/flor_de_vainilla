from pydantic import BaseModel

class customerCreate(BaseModel):
    name: str
    phone: str | None = None
    address: str | None = None

class CustomerResponse(BaseModel):

    customer_id: int
    name: str
    phone: str
    address: str | None = None

    class Config:

        from_attributes = True