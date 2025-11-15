import os
from typing import Generator

import pytest
from fastapi.testclient import TestClient


# ---------------------------------------------------------------------------
# Configuração de ambiente de TESTE
# ---------------------------------------------------------------------------
# Esses valores precisam ser definidos ANTES de importar qualquer coisa
# que use `services.config` ou `database.database`, para garantir que o
# engine e o Settings sejam construídos apontando para o banco de testes.
os.environ["ENVIRONMENT"] = "test"
os.environ.setdefault("SQLITE_DB_URL", "sqlite:///./pad_test.db")


from interfaces.api.config import create_app  # noqa: E402


@pytest.fixture(scope="session")
def client() -> Generator[TestClient, None, None]:
    """
    Cliente HTTP para testes de integração.
    """
    app = create_app()
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="session", autouse=True)
def _cleanup_test_db() -> Generator[None, None, None]:
    """
    Remove o arquivo de banco de testes ao final da suíte.
    """
    yield
    db_path = os.path.abspath("pad_test.db")
    if os.path.exists(db_path):
        os.remove(db_path)

