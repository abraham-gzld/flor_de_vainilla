from pydantic import BaseModel

class categoryCreate(BaseModel):
    name: str

class categoryResponse(BaseModel):

    category_id: int
    name: str

    class Config:

        from_attributes = True