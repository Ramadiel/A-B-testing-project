"""
Database Configuration
"""

import sqlalchemy as sql
import sqlalchemy.ext.declarative as declarative
import sqlalchemy.orm as orm
from dotenv import load_dotenv
import os

load_dotenv(".env")

DATABASE_URL = os.environ.get("DATABASE_URL")

engine = sql.create_engine(DATABASE_URL)

Base = declarative.declarative_base()

SessionLocal = orm.sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()
