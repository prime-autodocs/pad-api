from sqlalchemy import Column, Integer, Enum, String, TIMESTAMP, text
from sqlalchemy.sql.sqltypes import Date
from services.enums import CivilStatusEnum, GenderEnum, CustomerTypeEnum
from database.database import Base

class Customers(Base):
    __tablename__ = "customers"

    id = Column("id", Integer, primary_key=True, index=True)
    customer_type = Column("customer_type", Enum(CustomerTypeEnum), nullable=False)
    cpf_number = Column("cpf_number", String, nullable=False, unique=True)
    full_name = Column("full_name", String(255), nullable=False)
    gender = Column("gender", Enum(GenderEnum), nullable=False)
    email = Column("email", String(255), nullable=True)
    birth_date = Column("birth_date", Date, nullable=True)
    civil_status = Column("civil_status", Enum(CivilStatusEnum), nullable=False)
    tel_number = Column("tel_number", String, nullable=False)
    created_at = Column("created_at", TIMESTAMP(timezone=True), server_default=text("CURRENT_TIMESTAMP"), nullable=False)
    updated_at = Column("updated_at", TIMESTAMP(timezone=True), server_default=text("CURRENT_TIMESTAMP"), nullable=False)
    updated_by = Column("updated_by", String(255))