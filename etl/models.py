from sqlalchemy import Column, Integer, String, Text, BigInteger, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ABTesting(Base):
    __tablename__ = "ab_testing"

    test_id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    test_name = Column(Text, nullable=False)
    start_date = Column(Text, nullable=False)
    end_date = Column(Text, nullable=False)
    landing_page_id = Column(BigInteger, ForeignKey("landing_pages.landing_page_id"), nullable=False)
    product_id = Column(BigInteger, ForeignKey("products.product_id"), nullable=False)

    landing_page = relationship("LandingPage", back_populates="ab_tests")
    product = relationship("Product", back_populates="ab_tests")


class Customer(Base):
    __tablename__ = "customers"

    customer_id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    name = Column(Text, nullable=False)
    email = Column(Text, unique=True, index=True, nullable=False)


class LandingPage(Base):
    __tablename__ = "landing_pages"

    landing_page_id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    variant_type = Column(Text, nullable=False)
    page_url = Column(Text, nullable=False)
    product_id = Column(BigInteger, ForeignKey("products.product_id"), nullable=False)

    product = relationship("Product", back_populates="landing_pages")
    ab_tests = relationship("ABTesting", back_populates="landing_page")


class Product(Base):
    __tablename__ = "products"

    product_id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    product_name = Column(Text, nullable=False)
    category = Column(Text, nullable=False)
    description = Column(Text, nullable=True)
    logo_url = Column(Text, nullable=True)
    release_date = Column(Text, nullable=False)

    landing_pages = relationship("LandingPage", back_populates="product")
    ab_tests = relationship("ABTesting", back_populates="product")


class Result(Base):
    __tablename__ = "results"

    results_id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    click_through_rate = Column(Float, nullable=False)
    conversion_rate = Column(Float, nullable=False)
    bounce_rate = Column(Float, nullable=False)
    test_id = Column(BigInteger, ForeignKey("ab_testing.test_id"), nullable=False)

    ab_test = relationship("ABTesting")
