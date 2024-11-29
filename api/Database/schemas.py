from pydantic import BaseModel
from typing import Optional, List

# --- Customer Schemas ---

"""
Schemas for managing customer data. Includes models for retrieving, creating, 
and updating customer information.
"""

class Customer(BaseModel):
    """
    Schema for retrieving customer data from the database.
    """
    customer_id: int
    name: str
    email: str

    class Config:
        orm_mode = True


class CustomerCreate(BaseModel):
    """
    Schema for creating a new customer record.
    """
    name: str
    email: str


class CustomerUpdate(BaseModel):
    """
    Schema for updating existing customer data. Fields are optional to allow partial updates.
    """
    name: Optional[str] = None
    email: Optional[str] = None


# --- Product Schemas ---

"""
Schemas for managing product data. Includes models for retrieving, creating, 
and updating product information.
"""

class Product(BaseModel):
    """
    Schema for retrieving product data from the database.
    """
    product_id: int
    product_name: str
    category: str
    description: Optional[str] = None
    logo_url: Optional[str] = None
    release_date: str

    class Config:
        orm_mode = True


class ProductCreate(BaseModel):
    """
    Schema for creating a new product record.
    """
    product_name: str
    category: str
    description: Optional[str] = None
    logo_url: Optional[str] = None
    release_date: str


class ProductUpdate(BaseModel):
    """
    Schema for updating existing product data. Fields are optional to allow partial updates.
    """
    product_name: Optional[str] = None
    category: Optional[str] = None
    description: Optional[str] = None
    logo_url: Optional[str] = None
    release_date: Optional[str] = None


# --- AB Testing Schemas ---

"""
Schemas for managing A/B testing data. Includes models for retrieving, creating, 
and updating A/B testing experiments.
"""

class ABTest(BaseModel):
    """
    Schema for retrieving A/B testing data from the database.
    """
    test_id: int
    test_name: str
    start_date: str
    end_date: str
    landing_page_id: int
    product_id: int

    class Config:
        orm_mode = True


class ABTestCreate(BaseModel):
    """
    Schema for creating a new A/B testing experiment.
    """
    test_name: str
    start_date: str
    end_date: str
    landing_page_id: int
    product_id: int


class ABTestUpdate(BaseModel):
    """
    Schema for updating existing A/B testing data. Fields are optional to allow partial updates.
    """
    test_name: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    landing_page_id: Optional[int] = None
    product_id: Optional[int] = None

# --- Result Schemas ---

"""
Schemas for managing A/B testing result data. Includes models for retrieving, creating, 
and updating experiment results.
"""

class Result(BaseModel):
    """
    Schema for retrieving A/B testing result data from the database.
    """
    results_id: int
    click_through_rate: float
    conversion_rate: float
    bounce_rate: float
    test_id: int

    class Config:
        orm_mode = True


class ResultCreate(BaseModel):
    """
    Schema for creating a new result record for an A/B test.
    """
    click_through_rate: float
    conversion_rate: float
    bounce_rate: float
    test_id: int


class ResultUpdate(BaseModel):
    """
    Schema for updating existing result data for an A/B test. Fields are optional to allow partial updates.
    """
    click_through_rate: Optional[float] = None
    conversion_rate: Optional[float] = None
    bounce_rate: Optional[float] = None
    test_id: Optional[int] = None
