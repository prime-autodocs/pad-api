from sqlalchemy import Column, Integer, Enum, String, TIMESTAMP, text
from services.enums import FuelEnum
from database.database import Base

class Vehicles(Base):
    __tablename__ = "vehicles"

    id = Column("id", Integer, primary_key=True, index=True)
    customer_id = Column("customer_id", Integer, nullable=True)
    brand = Column("brand", String(255))
    model = Column("model", String(255))
    number_plate = Column("number_plate")
    chassis = Column("chassis", String(255))
    national_registry = Column("national_registry", String(255))
    year_fabric = Column("year_fabric", String(4))
    year_model = Column("year_model", String(4))
    fuel = Column("fuel", Enum(FuelEnum))
    color = Column("color", String(255))
    category = Column("category", String(255))
    certification_number = Column("certification_number", String(255))
    crlv_image = Column("crlv_image", String(255))
    created_at = Column("created_at", TIMESTAMP(timezone=True), server_default=text("CURRENT_TIMESTAMP"), nullable=False)
    updated_at = Column("updated_at", TIMESTAMP(timezone=True), server_default=text("CURRENT_TIMESTAMP"), nullable=False)
    updated_by = Column("updated_by", String(255))