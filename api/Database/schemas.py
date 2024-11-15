from pydantic import BaseModel

class Customer(BaseModel):
    customer_id: int
    name: str
    email: str

    class Config:
        orm_mode = True

class CustomerCreate(BaseModel):
    name: str
    email: str

class CustomerUpdate(BaseModel):
    name: str
    email: str
