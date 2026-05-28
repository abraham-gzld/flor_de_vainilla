from pydantic import BaseModel

class cakeExtraCreate(BaseModel):

    cake_id: int
    extra_id: int


class cakeExtraResponse(cakeExtraCreate):

    class Config:
        from_attributes = True