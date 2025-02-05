import re
from database.models.vehicles import Vehicles


def vehicle_data_validation(payload: Vehicles) -> dict:
    
    errors = []
    # Chassis
    chassis = payload.chassis
    # Rule 1: The first digit cannot be '0'
    if chassis[0] == '0':
        errors.append("Chassi inválido. Não pode começar com o número 0")
    
    # Rule 2: There cannot be consecutive repetition of the same digit more than six times
    if re.search(r'(.)\1{6,}', chassis):
        errors.append("Chassi inválido. Não pode ter 6 dígitos consecutivos")
    
    # Rule 3: Cannot contain the prohibited characters
    if re.search(r'[iIoOqQ]', chassis):
        errors.append("Chassi inválido. Não pode conter seguintes caracteres:  Q, O ou I")
        
    # Number Plate
    number_plate = payload.number_plate
    if not re.fullmatch(r'^[A-Z]{3}-?\d[A-Z0-9]\d{2}$', number_plate):
        errors.append("Placa inválida. Placa não apresenta o padrão brasileiro.")
        
    # National registry
    national_registry = payload.national_registry
    if len(national_registry) != 11:
        errors.append("Renavam inválido. Não pode conter mais que 11 caracteres")
    
    return {"is_valid": not errors, "errors": errors}