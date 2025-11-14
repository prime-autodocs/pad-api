from interfaces.api.schemas.feature_flags import FeatureFlagsSchema
from database.queries.feature_flags import FeatureFlagsQueries


class FeatureFlags:
    """
    Camada de orquestração para os feature flags.
    """

    # nomes das features exatamente como serão armazenadas no banco
    _FEATURE_KEYS = {
        "clientes-cadastrados": "clientes_cadastrados",
        "veiculos-cadastrados": "veiculos_cadastrados",
        "novos-clientes-resumo": "novos_clientes_resumo",
        "servicos-realizados-resumo": "servicos_realizados_resumo",
        "grafico-novos-clientes": "grafico_novos_clientes",
        "grafico-servicos-realizados": "grafico_servicos_realizados",
        "grafico-situacao-vistorias": "grafico_situacao_vistorias",
        "grafico-situacao-cnh": "grafico_situacao_cnh",
        "painel-pedidos-em-andamento": "painel_pedidos_em_andamento",
    }

    @classmethod
    def get_all_flags(cls) -> FeatureFlagsSchema:
        """
        Busca todos os feature flags no banco e retorna um objeto tipado.
        Qualquer flag ausente no banco volta como False.
        """
        flags_from_db = FeatureFlagsQueries.get_all_flags()

        payload = {}
        for db_key, schema_key in cls._FEATURE_KEYS.items():
            payload[schema_key] = bool(flags_from_db.get(db_key, False))

        return FeatureFlagsSchema(**payload)


