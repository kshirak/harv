from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

# Import the database URL from config.py
from app.core.config import DATABASE_URL

# Create the database engine with appropriate configuration
# For SQLite: use connect_args with check_same_thread=False
# For PostgreSQL: use production-ready pool and connection settings
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False}
    )
else:
    # PostgreSQL configuration - optimized for cloud deployments (Render, etc.)
    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,  # Verify connections are alive before using
        pool_recycle=3600,   # Recycle connections after 1 hour (Render may drop after inactivity)
        pool_size=5,         # Number of connections to maintain in the pool
        max_overflow=10,     # Allow up to 10 additional connections beyond pool_size
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