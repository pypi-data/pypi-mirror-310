from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import Tuple
from sqlalchemy.ext.declarative import DeclarativeMeta

# Define global variables to hold the session and engine
SessionLocal = None
engine = None

def db_connection(DATABASE_URL: str) -> Tuple:
    """
    Initialize the database engine and sessionmaker.
    """
    global engine, SessionLocal  # Make engine and SessionLocal accessible globally
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return engine, SessionLocal


def get_db():
    """
    Dependency function to provide database sessions.
    """
    if SessionLocal is None:
        raise Exception("SessionLocal is not initialized. Call db_connection first.")
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_all_tables(engine, Base: DeclarativeMeta):
    """
    Create all database tables.
    """
    Base.metadata.create_all(bind=engine)
