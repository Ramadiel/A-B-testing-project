from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException
from typing import List
from Database.models import CustomerDB, ProductDB, ABTestingDB, ResultDB, Base
from Database.schemas import (Customer, CustomerCreate, CustomerUpdate, Product, ProductCreate, ProductUpdate,
                              ABTest, ABTestCreate, ABTestUpdate, Result, ResultCreate, ResultUpdate)
from Database.database import get_db

app = FastAPI()


# --- Customer Endpoints ---
@app.get("/customers/{customer_id}", response_model=Customer)
async def get_customer(customer_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a specific customer by their ID.

    Args:
        customer_id (int): ID of the customer to retrieve.
        db (Session): Database session dependency.

    Returns:
        Customer: The details of the requested customer.

    Raises:
        HTTPException: If the customer is not found.
    """
    customer = db.query(CustomerDB).filter(CustomerDB.customer_id == customer_id).first()
    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

@app.post("/customers/", response_model=Customer)
async def create_customer(customer: CustomerCreate, db: Session = Depends(get_db)):
    """
    Create a new customer record.

    Args:
        customer (CustomerCreate): The details of the customer to create.
        db (Session): Database session dependency.

    Returns:
        Customer: The newly created customer record.
    """
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
    """
    Update an existing customer's details.

    Args:
        customer_id (int): ID of the customer to update.
        customer (CustomerUpdate): The updated details of the customer.
        db (Session): Database session dependency.

    Returns:
        Customer: The updated customer record.

    Raises:
        HTTPException: If the customer is not found.
    """
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
    """
    Delete a customer by their ID.

    Args:
        customer_id (int): ID of the customer to delete.
        db (Session): Database session dependency.

    Returns:
        dict: A confirmation message upon successful deletion.

    Raises:
        HTTPException: If the customer is not found.
    """
    customer = db.query(CustomerDB).filter(CustomerDB.customer_id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    db.delete(customer)
    db.commit()
    return {"message": "Customer deleted successfully"}

@app.get("/customers/", response_model=List[Customer])
async def get_all_customers(db: Session = Depends(get_db)):
    """
    Retrieve a list of all customers in the database.

    Args:
        db (Session): Database session dependency to query the database.

    Returns:
        List[Customer]: A list of all customers.
    """
    customers = db.query(CustomerDB).all()
    return customers


# --- Product Endpoints ---
@app.get("/products/{product_id}", response_model=Product)
async def get_product(product_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a specific product by its ID.

    Args:
        product_id (int): ID of the product to retrieve.
        db (Session): Database session dependency.

    Returns:
        Product: The details of the requested product.

    Raises:
        HTTPException: If the product is not found.
    """
    product = db.query(ProductDB).filter(ProductDB.product_id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.post("/products/", response_model=Product)
async def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    """
    Create a new product record.

    Args:
        product (ProductCreate): The details of the product to create.
        db (Session): Database session dependency.

    Returns:
        Product: The newly created product record.
    """
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
    """
    Update an existing product's details.

    Args:
        product_id (int): ID of the product to update.
        product (ProductUpdate): The updated details of the product.
        db (Session): Database session dependency.

    Returns:
        Product: The updated product record.

    Raises:
        HTTPException: If the product is not found.
    """
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
    """
    Delete a product by its ID.

    Args:
        product_id (int): ID of the product to delete.
        db (Session): Database session dependency.

    Returns:
        dict: A confirmation message upon successful deletion.

    Raises:
        HTTPException: If the product is not found.
    """
    product = db.query(ProductDB).filter(ProductDB.product_id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(product)
    db.commit()
    return {"message": "Product deleted successfully"}

@app.get("/products/", response_model=List[Product])
async def get_all_products(db: Session = Depends(get_db)):
    """
    Retrieve a list of all products in the database.

    Args:
        db (Session): Database session dependency to query the database.

    Returns:
        List[Product]: A list of all products.
    """
    products = db.query(ProductDB).all()
    return products


# --- AB Testing Endpoints ---
@app.get("/abtests/{test_id}", response_model=ABTest)
async def get_ab_test(test_id: int, db: Session = Depends(get_db)):
    """
    Retrieve an AB test by its ID.

    Args:
        id (int): The ID of the AB test.
        db (Session): Database session dependency to query the database.

    Returns:
        ABTest: The AB test record.
    """
    ab_test = db.query(ABTestingDB).filter(ABTestingDB.test_id == test_id).first()
    if ab_test is None:
        raise HTTPException(status_code=404, detail="AB Test not found")
    return ab_test

@app.post("/abtests/", response_model=ABTest)
async def create_ab_test(ab_test: ABTestCreate, db: Session = Depends(get_db)):
    """
    Create a new A/B test in the database, manually assigning an ID.
    """
    max_id = db.query(ABTestingDB.test_id).order_by(ABTestingDB.test_id.desc()).first()
    next_id = max_id[0] + 1 if max_id else 1

    new_ab_test = ABTestingDB(
        test_id=next_id,
        test_name=ab_test.test_name,
        start_date=ab_test.start_date,
        end_date=ab_test.end_date,
        landing_page_id=ab_test.landing_page_id,
        product_id=ab_test.product_id,
    )
    
    db.add(new_ab_test)
    db.commit()
    db.refresh(new_ab_test)
    
    return new_ab_test


@app.put("/abtests/{test_id}", response_model=ABTest)
async def update_ab_test(test_id: int, ab_test: ABTestUpdate, db: Session = Depends(get_db)):
    """
    Update an existing A/B test record.
    
    Args:
        test_id (int): The ID of the A/B test to update.
        ab_test (ABTestUpdate): Schema with updated values.
        db (Session): Database session dependency.
    
    Returns:
        ABTest: The updated A/B test record.
    """
    existing_ab_test = db.query(ABTestingDB).filter(ABTestingDB.test_id == test_id).first()

    if not existing_ab_test:
        raise HTTPException(status_code=404, detail="A/B test not found")

    if ab_test.test_name is not None:
        existing_ab_test.test_name = ab_test.test_name
    if ab_test.start_date is not None:
        existing_ab_test.start_date = ab_test.start_date
    if ab_test.end_date is not None:
        existing_ab_test.end_date = ab_test.end_date
    if ab_test.landing_page_id is not None:
        existing_ab_test.landing_page_id = ab_test.landing_page_id
    if ab_test.product_id is not None:
        existing_ab_test.product_id = ab_test.product_id

    db.commit()
    db.refresh(existing_ab_test)

    return existing_ab_test


@app.delete("/abtests/{test_id}")
async def delete_ab_test(test_id: int, db: Session = Depends(get_db)):
    """
    Delete an AB test by its ID.

    Args:
        abtest_id (int): ID of the AB test to delete.
        db (Session): Database session dependency.

    Returns:
        dict: A confirmation message upon successful deletion.

    Raises:
        HTTPException: If the AB test is not found.
    """
    ab_test = db.query(ABTestingDB).filter(ABTestingDB.test_id == test_id).first()
    if not ab_test:
        raise HTTPException(status_code=404, detail="AB Test not found")

    db.delete(ab_test)
    db.commit()
    return {"message": "AB Test deleted successfully"}

@app.get("/abtests/", response_model=List[ABTest])
async def get_all_ab_tests(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve a list of all AB tests with optional pagination.

    Args:
        skip (int): Number of records to skip.
        limit (int): Number of records to retrieve.
        db (Session): Database session dependency to query the database.

    Returns:
        List[ABTest]: A list of AB test records.
    """
    ab_tests = db.query(ABTestingDB).offset(skip).limit(limit).all()
    return ab_tests


# --- Result Endpoints ---
@app.get("/results/{results_id}", response_model=Result)
async def get_result(results_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a specific result by its ID.

    Args:
        result_id (int): ID of the result to retrieve.
        db (Session): Database session dependency.

    Returns:
        Result: The details of the requested result.

    Raises:
        HTTPException: If the result is not found.
    """
    result = db.query(ResultDB).filter(ResultDB.results_id == results_id).first()
    if result is None:
        raise HTTPException(status_code=404, detail="Result not found")
    return result

@app.post("/results/", response_model=Result)
async def create_result(result: ResultCreate, db: Session = Depends(get_db)):
    """
    Create a new result record for an A/B test, manually assigning an ID.
    """
    max_id = db.query(ResultDB.results_id).order_by(ResultDB.results_id.desc()).first()
    next_id = max_id[0] + 1 if max_id else 1

    new_result = ResultDB(
        results_id=next_id,
        click_through_rate=result.click_through_rate,
        conversion_rate=result.conversion_rate,
        bounce_rate=result.bounce_rate,
        test_id=result.test_id,
    )
    
    db.add(new_result)
    db.commit()
    db.refresh(new_result)
    
    return new_result

@app.put("/results/{result_id}", response_model=Result)
async def update_result(result_id: int, result: ResultUpdate, db: Session = Depends(get_db)):
    """
    Update an existing result record for an A/B test.
    
    Args:
        result_id (int): The ID of the result record to update.
        result (ResultUpdate): Schema with updated result values.
        db (Session): Database session dependency.
    
    Returns:
        Result: The updated result record.
    """
    existing_result = db.query(ResultDB).filter(ResultDB.results_id == result_id).first()
    
    if not existing_result:
        raise HTTPException(status_code=404, detail="Result not found")

    if result.click_through_rate is not None:
        existing_result.click_through_rate = result.click_through_rate
    if result.conversion_rate is not None:
        existing_result.conversion_rate = result.conversion_rate
    if result.bounce_rate is not None:
        existing_result.bounce_rate = result.bounce_rate
    if result.test_id is not None:
        existing_result.test_id = result.test_id
    
    db.commit()
    db.refresh(existing_result)
    
    return existing_result

@app.delete("/results/{results_id}")
async def delete_result(results_id: int, db: Session = Depends(get_db)):
    """
    Delete a result by its ID.

    Args:
        result_id (int): ID of the result to delete.
        db (Session): Database session dependency.

    Returns:
        dict: A confirmation message upon successful deletion.

    Raises:
        HTTPException: If the result is not found.
    """
    result = db.query(ResultDB).filter(ResultDB.results_id == results_id).first()
    if not result:
        raise HTTPException(status_code=404, detail="Result not found")

    db.delete(result)
    db.commit()
    return {"message": "Result deleted successfully"}

@app.get("/results/", response_model=List[Result])
async def get_all_results(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve a list of all results in the database with pagination.

    Args:
        skip (int): Number of records to skip.
        limit (int): Number of records to retrieve.
        db (Session): Database session dependency to query the database.

    Returns:
        List[Result]: A list of result records.
    """
    results = db.query(ResultDB).offset(skip).limit(limit).all()
    return results
