
from sqlalchemy import Column, Integer, String, TIMESTAMP, text
from sqlalchemy.sql.sqltypes import Date

from database.base import Base


class Users(Base):
    
    __tablename__ = "users"
    
    id = Column("id", Integer, primary_key=True, index=True)
    login = Column("login", String(255), nullable=False, unique=True)
    password = Column("password", String(255), nullable=False)
    username = Column("username", String(255), nullable=False)
    email = Column("email", String(255), nullable=False)
    last_login = Column("last_login", Date, nullable=True)
    created_at = Column("created_at", TIMESTAMP(timezone=True), server_default=text("CURRENT_TIMESTAMP"), nullable=False)
    updated_at = Column("updated_at", TIMESTAMP(timezone=True), server_default=text("CURRENT_TIMESTAMP"), nullable=False)