from sqlalchemy import Column, String, Boolean

from database.base import Base


class FeatureFlags(Base):
    __tablename__ = "feature_flags"

    feature_name = Column("feature_name", String(255), primary_key=True, index=True)
    switch = Column("switch", Boolean, nullable=False, default=False)


