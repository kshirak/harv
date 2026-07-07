from sqlalchemy import (
    Column,
    Integer,
    Float,
    DateTime,
    ForeignKey
)
from sqlalchemy.sql import func

from app.core.database import Base


class Telemetry(Base):
    __tablename__ = "telemetry"

    id = Column(Integer, primary_key=True)

    device_id = Column(Integer, ForeignKey("devices.id"))

    speed = Column(Float)

    rpm = Column(Float)

    battery = Column(Float)

    voltage = Column(Float)

    temperature = Column(Float)

    latitude = Column(Float)

    longitude = Column(Float)

    timestamp = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )