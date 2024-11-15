from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base, engine

Base = declarative_base()


# Define the Customer table
class Customer(Base):
    __tablename__ = "customers"

    customer_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    address = Column(String)
    city = Column(String)
    zip_code = Column(String)
    email = Column(String, unique=True)

# Define the Product table
class Product(Base):
    __tablename__ = "products"

    product_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    logo_url = Column(String)
    category = Column(String)
    release_date = Column(DateTime)

# Define the LandingPage table
class LandingPage(Base):
    __tablename__ = "landing_pages"

    landing_page_id = Column(Integer, primary_key=True)
    variant_type = Column(String)
    page_url = Column(String, unique=True)
    product_id = Column(Integer, ForeignKey("products.product_id"), nullable=False)

    product = relationship("Product", back_populates="landing_pages")
    ab_tests = relationship("ABTest", back_populates="landing_page")

# Define the ABTest table
class ABTest(Base):
    __tablename__ = "ab_tests"

    test_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    start_date = Column(DateTime, default=datetime.utcnow)
    end_date = Column(DateTime)
    landing_page_id = Column(Integer, ForeignKey("landing_pages.landing_page_id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.product_id"), nullable=False)

    landing_page = relationship("LandingPage", back_populates="ab_tests")
    product = relationship("Product", back_populates="ab_tests")
    results = relationship("TestResult", back_populates="test")

# Define the TestResult table
class TestResult(Base):
    __tablename__ = "test_results"

    result_id = Column(Integer, primary_key=True)
    click_through_rate = Column(Float)
    conversion_rate = Column(Float)
    bounce_rate = Column(Float)
    test_id = Column(Integer, ForeignKey("ab_tests.test_id"), nullable=False)

    test = relationship("ABTest", back_populates="results")

# Update relationships in Product class
Product.landing_pages = relationship("LandingPage", back_populates="product")
Product.ab_tests = relationship("ABTest", back_populates="product")

# Create all tables in the database
Base.metadata.create_all(engine)