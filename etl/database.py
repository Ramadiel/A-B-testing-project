"""
Database Configuration
"""

import sqlalchemy as sql
import sqlalchemy.ext.declarative as declarative
import sqlalchemy.orm as orm
from dotenv import load_dotenv
import os

load_dotenv(".env")

# Get the database URL from environment variables
DATABASE_URL = os.environ.get("DATABASE_URL")

# Create the SQLAlchemy engine
engine = sql.create_engine(DATABASE_URL)

# Base class for declarative models
Base = declarative.declarative_base()

# SessionLocal for database operations
SessionLocal = orm.sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Function to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Create all tables
def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()
