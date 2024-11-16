from pydantic import BaseModel
from typing import Optional

# Customer Schemas
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
    name: Optional[str] = None
    email: Optional[str] = None

# Product Schemas
class Product(BaseModel):
    product_id: int
    product_name: str
    category: str
    description: Optional[str] = None
    logo_url: Optional[str] = None
    release_date: str

    class Config:
        orm_mode = True

class ProductCreate(BaseModel):
    product_name: str
    category: str
    description: Optional[str] = None
    logo_url: Optional[str] = None
    release_date: str

class ProductUpdate(BaseModel):
    product_name: Optional[str] = None
    category: Optional[str] = None
    description: Optional[str] = None
    logo_url: Optional[str] = None
    release_date: Optional[str] = None
