import fastapi
from fastapi.middleware.cors import CORSMiddleware

from interfaces.api.routers.customers import router as customers
from interfaces.api.routers.vehicles import router as vehicles
from interfaces.api.routers.users import router as users

app = fastapi.FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],  
)

## Routers
app.include_router(customers, prefix="/customers", tags=["customers"])
app.include_router(vehicles, prefix="/vehicles", tags=["vehicles"])
app.include_router(users, prefix="/users", tags=["users"])