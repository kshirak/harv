from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.core.database import Base


class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"))

    vehicle_name = Column(String(100))

    vehicle_number = Column(String(50), unique=True)

    manufacturer = Column(String(100))

    model = Column(String(100))

    user = relationship("User")