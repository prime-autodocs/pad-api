from fastapi.testclient import TestClient


def test_feature_flags_endpoint_ok(client: TestClient) -> None:
    resp = client.get("/feature-flags/")

    assert resp.status_code == 200
    body = resp.json()

    # Deve conter todas as chaves definidas no schema
    expected_keys = {
        "clientes_cadastrados",
        "veiculos_cadastrados",
        "novos_clientes_resumo",
        "servicos_realizados_resumo",
        "grafico_novos_clientes",
        "grafico_servicos_realizados",
        "grafico_situacao_vistorias",
        "grafico_situacao_cnh",
        "painel_pedidos_em_andamento",
    }

    assert expected_keys.issubset(body.keys())


