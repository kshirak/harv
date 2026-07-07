from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

# Import the database URL from config.py
from app.core.config import DATABASE_URL

# Create the database engine (connection to SQLite)
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# Create a session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base class for all database models
Base = declarative_base()

# Dependency that provides a database session to API routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()