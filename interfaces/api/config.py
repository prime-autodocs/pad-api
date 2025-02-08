import fastapi

from interfaces.api.routers.customers import router as customers
from interfaces.api.routers.vehicles import router as vehicles
from interfaces.api.routers.users import router as users

app = fastapi.FastAPI()

## Routers
app.include_router(customers, prefix="/customers", tags=["customers"])
app.include_router(vehicles, prefix="/vehicles", tags=["vehicles"])
app.include_router(users, prefix="/users", tags=["users"])