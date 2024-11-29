from sqlalchemy import Column, Integer, String, Float, BigInteger, ForeignKey
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy.orm import relationship
from .database import Base

Base = declarative_base()

class ABTestingDB(Base):
    """
    Database model for A/B testing information.
    Represents the details of tests performed for landing pages and products.
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
    Stores information such as customer ID, name, and email.
    """
    __tablename__ = "customers"
    customer_id = Column(BigInteger, primary_key=True, index=True, nullable=False)
    name = Column(String, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)


class LandingPageDB(Base):
    """
    Database model for landing pages.
    Contains variant type, page URL, and associations with products and A/B tests.
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
    Stores product details such as name, category, description, logo, and release date.
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
    Stores metrics like click-through rate, conversion rate, and bounce rate for A/B tests.
    """
    __tablename__ = "results"

    results_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    click_through_rate = Column(Float, nullable=False)
    conversion_rate = Column(Float, nullable=False)
    bounce_rate = Column(Float, nullable=False)
    test_id = Column(Integer, ForeignKey("ab_testing.test_id"), nullable=False)

    # Relationships
    ab_test = relationship("ABTestingDB", back_populates="results")
