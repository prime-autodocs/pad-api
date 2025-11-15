from database.models.vehicles import Vehicles


def data_formatter(payload: Vehicles) -> Vehicles:
    """
    Normaliza campos textuais do veículo sem alterar os valores
    usados em enums (fuel/category).
    """

    if payload.brand and payload.brand != payload.brand.upper():
        payload.brand = payload.brand.upper()

    if payload.model and payload.model != payload.model.upper():
        payload.model = payload.model.upper()

    if payload.number_plate and payload.number_plate != payload.number_plate.upper():
        payload.number_plate = payload.number_plate.upper()

    if payload.color and payload.color != payload.color.upper():
        payload.color = payload.color.upper()

    if payload.chassis and payload.chassis != payload.chassis.upper():
        payload.chassis = payload.chassis.upper()

    # fuel e category são tratados via enums na camada de queries

    return payload