from sqlalchemy import create_engine, exc

from services.config import settings
from database.base import Base


def _create_engine():
    """
    Cria o engine do SQLAlchemy.

    - Em produção (ENVIRONMENT=production): usa POSTGRES_URL (ex.: MySQL).
    - Fora de produção: usa um banco SQLite local definido em SQLITE_DB_URL.
    """
    if settings.ENVIRONMENT == "production":
        if not settings.POSTGRES_URL:
            raise RuntimeError("POSTGRES_URL não está definido para o ambiente de produção.")

        return create_engine(
            settings.POSTGRES_URL,
            isolation_level="AUTOCOMMIT",
        )

    # Ambiente não-prod (development, staging, etc.): usar SQLite local
    return create_engine(
        settings.SQLITE_DB_URL,
        connect_args={"check_same_thread": False},
    )


def _init_sqlite_schema():
    """
    Cria as tabelas no banco SQLite local usando os models do SQLAlchemy.
    Apenas é executado quando não estamos em produção.
    """
    # Import atrasado para evitar referência circular:
    # os models importam Base deste módulo.
    from database.models.customers import Customers  # noqa: F401
    from database.models.customers_history import CustomersHistory  # noqa: F401
    from database.models.vehicles import Vehicles  # noqa: F401
    from database.models.vehicle_history import VehiclesHistory  # noqa: F401
    from database.models.users import Users  # noqa: F401
    from database.models.feature_flags import FeatureFlags  # noqa: F401

    Base.metadata.create_all(bind=engine)


engine = _create_engine()

# Se não for produção, garantir que o SQLite tenha o schema criado
if settings.ENVIRONMENT != "production":
    _init_sqlite_schema()