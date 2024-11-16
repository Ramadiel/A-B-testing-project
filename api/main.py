from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException
from typing import Dict
from Database.models import CustomerDB, ProductDB, Base
from Database.schemas import Customer, CustomerCreate, CustomerUpdate, Product, ProductCreate, ProductUpdate
from Database.database import get_db

app = FastAPI()

# Customer Endpoints
@app.get("/customers/{customer_id}", response_model=Customer)
async def get_customer(customer_id: int, db: Session = Depends(get_db)):
    customer = db.query(CustomerDB).filter(CustomerDB.customer_id == customer_id).first()
    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

@app.post("/customers/", response_model=Customer)
async def create_customer(customer: CustomerCreate, db: Session = Depends(get_db)):
    max_id = db.query(CustomerDB.customer_id).order_by(CustomerDB.customer_id.desc()).first()
    next_id = max_id[0] + 1 if max_id else 1

    new_customer = CustomerDB(
        customer_id=next_id,
        name=customer.name,
        email=customer.email
    )

    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)
    return new_customer

@app.put("/customers/{customer_id}", response_model=Customer)
async def update_customer(customer_id: int, customer: CustomerUpdate, db: Session = Depends(get_db)):
    existing_customer = db.query(CustomerDB).filter(CustomerDB.customer_id == customer_id).first()
    if not existing_customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    if customer.name:
        existing_customer.name = customer.name
    if customer.email:
        existing_customer.email = customer.email
    db.commit()
    db.refresh(existing_customer)
    return existing_customer

@app.delete("/customers/{customer_id}")
async def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    customer = db.query(CustomerDB).filter(CustomerDB.customer_id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    db.delete(customer)
    db.commit()
    return {"message": "Customer deleted successfully"}


# Product Endpoints
@app.get("/products/{product_id}", response_model=Product)
async def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(ProductDB).filter(ProductDB.product_id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.post("/products/", response_model=Product)
async def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    max_id = db.query(ProductDB.product_id).order_by(ProductDB.product_id.desc()).first()
    next_id = max_id[0] + 1 if max_id else 1

    new_product = ProductDB(
        product_id=next_id,
        product_name=product.product_name,
        category=product.category,
        description=product.description,
        logo_url=product.logo_url,
        release_date=product.release_date
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


@app.put("/products/{product_id}", response_model=Product)
async def update_product(product_id: int, product: ProductUpdate, db: Session = Depends(get_db)):
    existing_product = db.query(ProductDB).filter(ProductDB.product_id == product_id).first()
    if not existing_product:
        raise HTTPException(status_code=404, detail="Product not found")
    if product.product_name:
        existing_product.product_name = product.product_name
    if product.category:
        existing_product.category = product.category
    if product.description:
        existing_product.description = product.description
    if product.logo_url:
        existing_product.logo_url = product.logo_url
    if product.release_date:
        existing_product.release_date = product.release_date
    db.commit()
    db.refresh(existing_product)
    return existing_product

@app.delete("/products/{product_id}")
async def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(ProductDB).filter(ProductDB.product_id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(product)
    db.commit()
    return {"message": "Product deleted successfully"}
