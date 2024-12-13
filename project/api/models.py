"""
Database Models for the ETL Process.

This module defines the database models using SQLAlchemy for A/B testing, customers, products, and landing pages. These models represent the structure of the database tables and establish relationships between different entities required for an effective ETL (Extract, Transform, Load) process in an analytics or business environment.

Dependencies:
    - sqlalchemy: Used for defining the Object Relational Mapping (ORM) models and database schema.
    - pydantic: Typically used for data validation; however, it is not utilized directly in these models but can be applied in conjunction with the API layer.

Features:
1. **A/B Testing**: Tracks test configurations and results for various landing pages and products.
2. **Customers**: Stores customer information such as unique IDs, names, and email addresses.
3. **Products**: Maintains product details, including category, description, and associations with tests and landing pages.
4. **Landing Pages**: Defines landing page variants and links them to corresponding products and tests.
5. **Results**: Captures key performance indicators (KPIs) for A/B testing, such as click-through rate and conversion rate.

"""

from sqlalchemy import Column, Integer, String, Float, BigInteger, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from .database import Base

Base = declarative_base()

class ABTestingDB(Base):
    """
    Database model for A/B testing information.

    This table represents the details of A/B tests conducted to evaluate different landing page variants and product offerings. It stores metadata about each test and associates it with the related landing pages and products.

    Attributes:
        - test_id (Integer): Primary key for the A/B test.
        - test_name (String): Name or identifier of the test.
        - start_date (String): Test start date in YYYY-MM-DD format.
        - end_date (String): Test end date in YYYY-MM-DD format.
        - landing_page_id (Integer): Foreign key linking to the landing_pages table.
        - product_id (Integer): Foreign key linking to the products table.
    Relationships:
        - landing_page: Links to the LandingPageDB model.
        - product: Links to the ProductDB model.
        - results: Links to the ResultDB model for test outcomes.
    """
    __tablename__ = "ab_testing"

    test_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    test_name = Column(String, nullable=False)
    start_date = Column(String, nullable=False)
    end_date = Column(String, nullable=False)
    landing_page_id = Column(Integer, ForeignKey("landing_pages.landing_page_id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.product_id"), nullable=False)

    # Relationships
    landing_page = relationship("LandingPageDB", back_populates="ab_tests")
    product = relationship("ProductDB", back_populates="ab_tests")
    results = relationship("ResultDB", back_populates="ab_test", cascade="all, delete")


class CustomerDB(Base):
    """
    Database model for customers.

    This table stores information about the customers interacting with the platform. It includes unique identifiers, names, and contact details.

    Attributes:
        - customer_id (BigInteger): Primary key for the customer.
        - name (String): Customer's full name.
        - email (String): Customer's email address (unique).
    """
    __tablename__ = "customers"

    customer_id = Column(BigInteger, primary_key=True, index=True, nullable=False)
    name = Column(String, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)


class LandingPageDB(Base):
    """
    Database model for landing pages.

    This table defines different variants of landing pages used in marketing campaigns. Each page is linked to a product and is associated with various A/B tests.

    Attributes:
        - landing_page_id (Integer): Primary key for the landing page.
        - variant_type (String): The type of landing page variant (e.g., control, test).
        - page_url (String): URL of the landing page.
        - product_id (Integer): Foreign key linking to the products table.
    Relationships:
        - product: Links to the ProductDB model.
        - ab_tests: Links to the ABTestingDB model for associated tests.
    """
    __tablename__ = "landing_pages"

    landing_page_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    variant_type = Column(String, nullable=False)
    page_url = Column(String, nullable=False)
    product_id = Column(Integer, ForeignKey("products.product_id"), nullable=False)

    # Relationships
    product = relationship("ProductDB", back_populates="landing_pages")
    ab_tests = relationship("ABTestingDB", back_populates="landing_page", cascade="all, delete")


class ProductDB(Base):
    """
    Database model for products.

    This table stores information about the products being promoted or sold. Each product can have multiple associated landing pages and A/B tests.

    Attributes:
        - product_id (BigInteger): Primary key for the product.
        - product_name (String): Name of the product.
        - category (String): Category or type of product.
        - description (String): Brief description of the product (optional).
        - logo_url (String): URL of the product logo (optional).
        - release_date (String): Release date in YYYY-MM-DD format.
    Relationships:
        - landing_pages: Links to the LandingPageDB model for associated landing pages.
        - ab_tests: Links to the ABTestingDB model for associated tests.
    """
    __tablename__ = "products"

    product_id = Column(BigInteger, primary_key=True, index=True, nullable=False)
    product_name = Column(String, nullable=False)
    category = Column(String, nullable=False)
    description = Column(String, nullable=True)
    logo_url = Column(String, nullable=True)
    release_date = Column(String, nullable=False)

    # Relationships
    landing_pages = relationship("LandingPageDB", back_populates="product", cascade="all, delete")
    ab_tests = relationship("ABTestingDB", back_populates="product", cascade="all, delete")


class ResultDB(Base):
    """
    Database model for test results.

    This table stores the performance metrics of A/B tests conducted on landing pages and products. The metrics include click-through rates, conversion rates, and bounce rates.

    Attributes:
        - results_id (Integer): Primary key for the test result.
        - click_through_rate (Float): Percentage of users who clicked on the landing page.
        - conversion_rate (Float): Percentage of users who completed the desired action.
        - bounce_rate (Float): Percentage of users who left the page without engaging.
        - test_id (Integer): Foreign key linking to the ab_testing table.
    Relationships:
        - ab_test: Links to the ABTestingDB model for associated tests.
    """
    __tablename__ = "results"

    results_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    click_through_rate = Column(Float, nullable=False)
    conversion_rate = Column(Float, nullable=False)
    bounce_rate = Column(Float, nullable=False)
    test_id = Column(Integer, ForeignKey("ab_testing.test_id"), nullable=False)

    # Relationships
    ab_test = relationship("ABTestingDB", back_populates="results")
