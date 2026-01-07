import enum

@enum.unique
class CustomerTypeEnum(enum.Enum):
    """All type of customers"""
    DETRAN = "DETRAN"
    SMTR = "SMTR"
    both = "Ambos"

@enum.unique
class CivilStatusEnum(enum.Enum):
    """Civil status of the customer"""
    single = "Solteiro(a)"
    married = "Casado(a)"
    divorced = "Divorciado(a)"
    widowed = "Viúvo(a)"
    stable_union = "União Estável"

@enum.unique
class GenderEnum(enum.Enum):
    """Gender of the customer"""
    male = "Masculino"
    female = "Feminino"
    others = "Outros"
    
@enum.unique
class FuelEnum(enum.Enum):
    """Type of fuel of the vehicle"""
    alchool = 'alchool'
    gas = 'gas'
    gasoline = 'gasoline'
    alchool_gas = 'alchool_gas'
    gasoline_gas = 'gasoline_gas'
    diesel = 'diesel'
    electric = 'electric'

@enum.unique
class TaxTypeEnum(enum.Enum):
    """Type of tax id of the customer"""
    CPF = 'CPF'
    CNPJ = 'CNPJ'
