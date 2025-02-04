import re
from validate_docbr import CNPJ, CPF
from typing import Dict
from database.models.customers import Customers

def customer_data_validation(payload: Customers) -> Dict:
    errors = []

    # Full name validation
    if payload.full_name:
        full_name = payload.full_name.strip()
        if len(full_name.split()) < 2:
            errors.append("Nome completo deve conter pelo menos duas palavras.")

    # CPF and CNPJ validation
    if payload.tax_id and payload.tax_type:
        tax_id = payload.tax_id.strip()
        if payload.tax_type == "CNPJ":
            cnpj = CNPJ()
            if not cnpj.validate(tax_id):
                errors.append("CNPJ inválido ou incorreto. Deve conter 14 dígitos e ser válido.")
        elif payload.tax_type == "CPF":
            cpf = CPF()   
            if not cpf.validate(tax_id):
                errors.append("CPF inválido ou incorreto. Deve conter 11 dígitos e ser válido.")

    # Email validatiom
    if payload.email:
        email = payload.email.strip()
        if not re.fullmatch(r'[\w\.-]+@[\w\.-]+\.\w{2,}', email):
            errors.append("Email inválido. Deve conter um @ e um domínio válido.")

    # Telephone validation
    if payload.tel_number:
        tel_number = payload.tel_number.strip()
        tel_number_digits = ''.join(filter(str.isdigit, tel_number))
        if len(tel_number_digits) not in [10, 11]:
            errors.append("Telefone inválido. Deve ter 10 ou 11 dígitos.")

    return {"is_valid": not errors, "errors": errors}