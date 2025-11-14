from fastapi import APIRouter

from core.feature_flags import FeatureFlags
from interfaces.api.schemas.feature_flags import FeatureFlagsSchema


router = APIRouter()


@router.get("/", response_model=FeatureFlagsSchema)
async def get_feature_flags() -> FeatureFlagsSchema:
    """
    Endpoint para retornar todos os feature flags.

    A tabela no banco deve conter linhas com:
    - feature_name: str (ex.: 'clientes-cadastrados')
    - switch: bool
    """
    return FeatureFlags.get_all_flags()


