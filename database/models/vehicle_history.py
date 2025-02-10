from sqlalchemy import Column, Integer, String, TIMESTAMP, text
from database.database import Base

class VehiclesHistory(Base):
    __tablename__ = "vehicle_history"

    id = Column("id", Integer, primary_key=True, index=True)
    vehicle_id = Column("vehicle_id", Integer, nullable=False)
    updated_at = Column("updated_at", TIMESTAMP(timezone=True), server_default=text("CURRENT_TIMESTAMP"), nullable=False)
    updated_by = Column("updated_by", String(255))
    description = Column("description", String(255))