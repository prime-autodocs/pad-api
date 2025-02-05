from database.models.vehicles import Vehicles

def data_formatter(payload: Vehicles) -> Vehicles: 

    if payload.brand != payload.brand.upper():
        payload.brand = payload.brand.upper()

    if payload.model != payload.model.upper():
        payload.model = payload.model.upper()
    
    if payload.number_plate != payload.number_plate.upper():
        payload.number_plate = payload.number_plate.upper()
    
    if payload.color != payload.color.upper():
        payload.color = payload.color.upper()
    
    if payload.chassis != payload.chassis.upper():
        payload.chassis = payload.chassis.upper()
    
    if payload.category != payload.category.upper():
        payload.category = payload.category.upper()

    return payload