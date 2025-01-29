import re
from typing import Dict
from database.models.customers import Customers

def validate_cpf(cpf: str) -> bool:
    cpf = re.sub(r'\D', '', cpf)

    if len(cpf) != 11 or cpf == cpf[0] * len(cpf):
        return False

    def calculate_digit(cpf_partial: str, weight_start: int) -> int:
        weight = weight_start
        total = 0
        for digit in cpf_partial:
            total += int(digit) * weight
            weight -= 1
        remainder = total % 11
        return 0 if remainder < 2 else 11 - remainder

    first_digit = calculate_digit(cpf[:9], 10)
    second_digit = calculate_digit(cpf[:9] + str(first_digit), 11)

    return cpf[-2:] == f"{first_digit}{second_digit}"

def customer_data_validation(payload: Customers) -> Dict:
    errors = []

    # Full name validation
    full_name = payload.full_name.strip()
    if len(full_name.split()) < 2:
        errors.append("Nome completo deve conter pelo menos duas palavras.")

    # CPF validation
    cpf_number = payload.cpf_number.strip()
    if not re.fullmatch(r'\d{11}', cpf_number) or not validate_cpf(cpf_number):
        errors.append("CPF inválido ou incorreto. Deve conter 11 dígitos e ser válido.")

    # Email validatiom
    email = payload.email.strip()
    if not re.fullmatch(r'[\w\.-]+@[\w\.-]+\.\w{2,}', email):
        errors.append("Email inválido. Deve conter um @ e um domínio válido.")

    # Telephone validation
    tel_number = payload.tel_number.strip()
    tel_number_digits = ''.join(filter(str.isdigit, tel_number))
    if len(tel_number_digits) not in [10, 11]:
        errors.append("Telefone inválido. Deve ter 10 ou 11 dígitos.")

    return {"is_valid": not errors, "errors": errors}