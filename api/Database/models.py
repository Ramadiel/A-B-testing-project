from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Float, BigInteger, Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

Base = declarative_base()

class ABTestingDB(Base):
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

class CustomerDB(Base):
    __tablename__ = "customers"
    customer_id = Column(BigInteger, primary_key=True, index=True, nullable=False)
    name = Column(String, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)

class LandingPageDB(Base):
    __tablename__ = "landing_pages"

    landing_page_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    variant_type = Column(String, nullable=False)
    page_url = Column(String, nullable=False)
    product_id = Column(Integer, ForeignKey("products.product_id"), nullable=False)

    # Relationships
    product = relationship("ProductDB", back_populates="landing_pages")
    ab_tests = relationship("ABTestingDB", back_populates="landing_page", cascade="all, delete")

class ProductDB(Base):
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
    __tablename__ = "results"

    results_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    click_through_rate = Column(Float, nullable=False)
    conversion_rate = Column(Float, nullable=False)
    bounce_rate = Column(Float, nullable=False)
    test_id = Column(Integer, ForeignKey("ab_testing.test_id"), nullable=False)

    # Relationships
    ab_test = relationship("ABTestingDB", back_populates="results")

ABTestingDB.results = relationship("ResultDB", back_populates="ab_test", cascade="all, delete")
