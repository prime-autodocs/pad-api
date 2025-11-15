from sqlalchemy import Column, Integer, String, TIMESTAMP, text

from database.base import Base


class Address(Base):
    __tablename__ = "address"

    id = Column("id", Integer, primary_key=True, index=True)
    customer_id = Column("customer_id", Integer, nullable=False)
    address = Column("address", String(255))
    number = Column("number", String(20))
    complement = Column("complement", String(255))
    neighborhood = Column("neighborhood", String(255))
    city = Column("city", String(255))
    state = Column("state", String(2))
    zip_code = Column("zip_code", String(20))
    created_at = Column(
        "created_at",
        TIMESTAMP(timezone=True),
        server_default=text("CURRENT_TIMESTAMP"),
        nullable=False,
    )
    updated_at = Column(
        "updated_at",
        TIMESTAMP(timezone=True),
        server_default=text("CURRENT_TIMESTAMP"),
        nullable=False,
    )
    updated_by = Column("updated_by", String(255))


