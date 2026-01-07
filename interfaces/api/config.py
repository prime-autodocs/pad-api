import fastapi
from fastapi.middleware.cors import CORSMiddleware

from interfaces.api.routers.customers import router as customers
from interfaces.api.routers.vehicles import router as vehicles
from interfaces.api.routers.users import router as users
from interfaces.api.routers.auth import router as auth
from interfaces.api.routers.dashboards import router as dashboards
from interfaces.api.routers.feature_flags import router as feature_flags
from interfaces.api.routers.reports import router as reports


def create_app() -> fastapi.FastAPI:
    """
    Cria e configura a aplicação FastAPI (middlewares, CORS e routers).

    Essa função é usada pelo `main.py` para criar a variável global `app`.
    """
    app = fastapi.FastAPI()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Routers
    app.include_router(auth, prefix="/auth", tags=["auth"])
    app.include_router(users, prefix="/users", tags=["users"])
    app.include_router(customers, prefix="/customers", tags=["customers"])
    app.include_router(vehicles, prefix="/vehicles", tags=["vehicles"])
    app.include_router(dashboards, prefix="/dashboards", tags=["dashboards"])
    app.include_router(feature_flags, prefix="/feature-flags", tags=["feature-flags"])
    app.include_router(reports, prefix="/reports", tags=["reports"])

    return app
