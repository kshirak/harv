from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime

from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)
    place = Column(String, nullable=True)

    aadhar_number = Column(String, unique=True, nullable=True)
    phone_number = Column(String, unique=True, nullable=False)

    location = Column(String, nullable=False)
    acres_of_land = Column(Float, nullable=False)

    fin_id = Column(String, unique=True, nullable=False, index=True)

    hashed_password = Column(String, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)