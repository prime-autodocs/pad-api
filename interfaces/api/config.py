import fastapi

from interfaces.api.routers.customers import router as customers

app = fastapi.FastAPI()

## Routers
app.include_router(customers, prefix="/customers", tags=["customers"])
