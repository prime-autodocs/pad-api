from typing import Dict

from database.session import db_session
from database.models.feature_flags import FeatureFlags


class FeatureFlagsQueries:
    table = FeatureFlags

    @classmethod
    def get_all_flags(cls) -> Dict[str, bool]:
        """
        Retorna todos os feature flags como um dicionário:
        {feature_name: switch}
        """
        with db_session() as db:
            rows = db.query(FeatureFlags).all()
            flags: Dict[str, bool] = {}
            for row in rows:
                flags[row.feature_name] = bool(row.switch)
            return flags


