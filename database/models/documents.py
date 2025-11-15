from sqlalchemy import Column, Integer, String, TIMESTAMP, Date, text

from database.base import Base


class Documents(Base):
    __tablename__ = "documents"

    id = Column("id", Integer, primary_key=True, index=True)
    customer_id = Column("customer_id", Integer, nullable=False, unique=True)
    identity_number = Column("identity_number", String(255))
    identity_org = Column("identity_org", String(255))
    identity_issued_at = Column("identity_issued_at", Date)
    identity_local = Column("identity_local", String(255))
    driver_license_number = Column("driver_license_number", String(255))
    driver_license_expiration = Column("driver_license_expiration", Date)
    driver_license_image = Column("driver_license_image", String(255))
    smtr_permission_number = Column("smtr_permission_number", String(255))
    smtr_permission_image = Column("smtr_permission_image", String(255))
    smtr_ratr_number = Column("smtr_ratr_number", String(255))
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


