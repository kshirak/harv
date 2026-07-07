from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from app.core.database import Base


class Device(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, index=True)

    vehicle_id = Column(Integer, ForeignKey("vehicles.id"))

    device_id = Column(String(100), unique=True)

    device_secret = Column(String(255))

    firmware_version = Column(String(20))

    is_online = Column(Boolean, default=False)

    vehicle = relationship("Vehicle")