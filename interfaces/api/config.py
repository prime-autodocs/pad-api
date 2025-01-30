import fastapi

from interfaces.api.routers.customers import router as customers
from interfaces.api.routers.vehicles import router as vehicles

app = fastapi.FastAPI()

## Routers
app.include_router(customers, prefix="/customers", tags=["customers"])
app.include_router(vehicles, prefix="/vehicles", tags=["vehicles"])