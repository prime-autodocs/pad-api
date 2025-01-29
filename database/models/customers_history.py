from sqlalchemy import Column, Integer, String, TIMESTAMP, text
from database.database import Base

class CustomersHistory(Base):
    __tablename__ = "customers_history"

    id = Column("id", Integer, primary_key=True, index=True)
    customer_id = Column("customer_id", Integer, nullable=False)
    updated_at = Column("updated_at", TIMESTAMP(timezone=True), server_default=text("CURRENT_TIMESTAMP"), nullable=False)
    updated_by = Column("updated_by", String(255))
    column_change = Column("column_change", String(255))