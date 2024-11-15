from sqlalchemy import Column, Integer, String, Text, BigInteger, Float, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class ABTestingDB(Base):
    __tablename__ = "ab_testing"

    test_id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    test_name = Column(Text, nullable=False)
    start_date = Column(Text, nullable=False)
    end_date = Column(Text, nullable=False)
    landing_page_id = Column(BigInteger, ForeignKey("landing_pages.landing_page_id"), nullable=False)
    product_id = Column(BigInteger, ForeignKey("products.product_id"), nullable=False)

    # Relationships
    landing_page = relationship("LandingPageDB", back_populates="ab_tests")
    product = relationship("ProductDB", back_populates="ab_tests")

class CustomerDB(Base):
    __tablename__ = "customers"

    customer_id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    name = Column(Text, index=True, nullable=False)
    email = Column(Text, unique=True, index=True, nullable=False)

class LandingPageDB(Base):
    __tablename__ = "landing_pages"

    landing_page_id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    variant_type = Column(Text, nullable=False)
    page_url = Column(Text, nullable=False)
    product_id = Column(BigInteger, ForeignKey("products.product_id"), nullable=False)

    # Relationships
    product = relationship("ProductDB", back_populates="landing_pages")
    ab_tests = relationship("ABTestingDB", back_populates="landing_page", cascade="all, delete")

class ProductDB(Base):
    __tablename__ = "products"

    product_id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    product_name = Column(Text, nullable=False)
    category = Column(Text, nullable=False)
    description = Column(Text, nullable=True)
    logo_url = Column(Text, nullable=True)
    release_date = Column(Text, nullable=False)

    # Relationships
    landing_pages = relationship("LandingPageDB", back_populates="product", cascade="all, delete")
    ab_tests = relationship("ABTestingDB", back_populates="product", cascade="all, delete")

class ResultDB(Base):
    __tablename__ = "results"

    results_id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    click_through_rate = Column(Float, nullable=False)
    conversion_rate = Column(Float, nullable=False)
    bounce_rate = Column(Float, nullable=False)
    test_id = Column(BigInteger, ForeignKey("ab_testing.test_id"), nullable=False)

    # Relationships
    ab_test = relationship("ABTestingDB", back_populates="results")

ABTestingDB.results = relationship("ResultDB", back_populates="ab_test", cascade="all, delete")
