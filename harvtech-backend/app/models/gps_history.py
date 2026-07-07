from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.sql import func

from app.core.database import Base


class GPSHistory(Base):
    __tablename__ = "gps_history"

    id = Column(Integer, primary_key=True)

    vehicle_id = Column(Integer, ForeignKey("vehicles.id"))

    latitude = Column(Float)

    longitude = Column(Float)

    timestamp = Column(DateTime(timezone=True), server_default=func.now())