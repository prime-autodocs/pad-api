from pydantic import BaseModel


class FeatureFlagsSchema(BaseModel):
    clientes_cadastrados: bool
    veiculos_cadastrados: bool
    novos_clientes_resumo: bool
    servicos_realizados_resumo: bool
    grafico_novos_clientes: bool
    grafico_servicos_realizados: bool
    grafico_situacao_vistorias: bool
    grafico_situacao_cnh: bool
    painel_pedidos_em_andamento: bool


