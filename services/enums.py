import enum
from typing import Optional

@enum.unique
class CustomerTypeEnum(enum.Enum):
    """All type of customers"""
    DETRAN = "DETRAN"
    SMTR = "SMTR"
    both = "both"

@enum.unique
class CivilStatusEnum(enum.Enum):
    """Civil status of the customer"""
    single = "single"
    married = "married"
    divorced = "divorced"
    widowed = "widowed"

@enum.unique
class GenderEnum(enum.Enum):
    """Gender of the customer"""
    male = "male"
    female = "female"
    others = "others"
