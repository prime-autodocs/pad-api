## PrimeAutoDocs API

API em FastAPI para gestão de clientes, veículos e relatórios da PrimeAutoDocs, com suporte a autenticação, dashboards, feature flags e relatórios analíticos.

### Stack principal

- **Linguagem**: Python 3.11
- **Framework web**: FastAPI
- **ORM**: SQLAlchemy 2
- **Banco (produção)**: PostgreSQL (`POSTGRES_URL`)
- **Banco (dev)**: SQLite local (`pad_local.db`)
- **Servidor ASGI**: Uvicorn

### Estrutura do projeto

- `main.py`: ponto de entrada da aplicação, cria a instância `app` e sobe o servidor.
- `interfaces/api/config.py`: configuração da aplicação FastAPI (CORS, inclusão de routers).
- `interfaces/api/routers/`: definição das rotas HTTP.
  - `auth.py`: autenticação.
  - `customers.py`: CRUD de clientes.
  - `vehicles.py`: CRUD de veículos.
  - `users.py`: login de usuários.
  - `dashboards.py`: métricas para cards e gráficos de dashboard.
  - `feature_flags.py`: leitura de feature flags.
  - `reports.py`: relatórios (lista de clientes x veículos, detalhes de cliente).
- `interfaces/api/schemas/`: modelos Pydantic (request/response).
- `core/`: camada de orquestração/regra de negócio.
- `database/`:
  - `database.py`: criação do `engine` e bootstrap do schema em SQLite.
  - `session.py`: criação de sessões (`SessionLocal`, `db_session`, `get_db`).
  - `models/`: models SQLAlchemy (`customers`, `vehicles`, `users`, `documents`, `address`, etc.).
  - `queries/`: camada de acesso a dados usando os models.
- `services/`:
  - `config.py`: leitura de variáveis de ambiente (`Settings`).
  - `enums.py`: enums de domínio (tipos de cliente, combustível, etc.).
  - `utils/`: validações e formatadores de dados.

### Configuração de ambiente

Crie um arquivo `.env` na raiz com, no mínimo:

```env
ENVIRONMENT=development            # production para usar PostgreSQL

API_HOST=0.0.0.0
LOG_LEVEL=debug
RELOAD=true

# Banco de dados
POSTGRES_URL=postgresql+psycopg2://user:password@host:5432/db_name
SQLITE_DB_URL=sqlite:///./pad_local.db
```

- Em **produção** (`ENVIRONMENT=production`): a API usa `POSTGRES_URL`.
- Em **desenvolvimento** (outro valor ou não definido): usa `SQLITE_DB_URL` e cria automaticamente as tabelas no `pad_local.db`.

### Instalando dependências

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
```

### Executando localmente

```bash
python main.py --mode api
```

Por padrão a API sobe em `http://API_HOST:8000` (ex.: `http://0.0.0.0:8000`) com:

- Documentação interativa: `http://localhost:8000/docs`

Você também pode subir diretamente com uvicorn:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Conexão com banco e sessões

- O `engine` é criado em `database/database.py`, escolhendo PostgreSQL ou SQLite de acordo com `ENVIRONMENT`.
- As sessões são gerenciadas em `database/session.py`:
  - `SessionLocal` com `expire_on_commit=False` para evitar erros de sessão expirada.
  - `db_session()` para uso interno nas queries (abre/fecha/rollback).
  - `get_db()` para usar como dependência do FastAPI, se necessário.

### Endpoints principais (visão geral)

- **Auth**
  - `GET /auth/` – login (validação de usuário/senha).
- **Customers**
  - `GET /customers/` – lista clientes.
  - `GET /customers/{customer_id}` – detalhe de cliente.
  - `GET /customers/tax_id/{tax_id}` – busca por CPF/CNPJ.
  - `POST /customers/` – criação de cliente **com** `address` e `documents`:
    - payload segue o modelo `CustomerCreateWithDetails`.
  - `PATCH /customers/{customer_id}` – atualização de cliente.
  - `DELETE /customers/{customer_id}` – exclusão de cliente.
- **Vehicles**
  - `GET /vehicles/?customer_id=...` – lista veículos de um cliente.
  - `GET /vehicles/{vehicle_id}` – detalhe do veículo.
  - `POST /vehicles/`, `PATCH /vehicles/{vehicle_id}`, `DELETE /vehicles/{vehicle_id}` – CRUD.
- **Dashboards**
  - `GET /dashboards/cards-summary` – cards de números principais (clientes, veículos, novos clientes, serviços).
  - `GET /dashboards/new-customers?period=monthly|quarter|annual` – série temporal de novos clientes.
- **Feature Flags**
  - `GET /feature-flags/` – retorna todas as flags (clientes, gráficos, painéis) com `true/false`.
- **Reports**
  - `GET /reports/list?search=&filter_by=` – relatório de clientes com quantidade de veículos:
    - `search`: nome, CPF/CNPJ ou placa.
    - `filter_by`: tipo de cliente (`DETRAN`, `SMTR`, `both`).
    - resposta: `items[]` + `total_clients`.
  - `GET /reports/customer-details/{customer_id}` – detalhes completos do cliente:
    - dados do cliente na raiz (`id`, `full_name`, `tax_id`, etc.).
    - chaves aninhadas `address` e `documents`.

### Convenções de código

- Validações de domínio ficam em `services/utils/*_validation.py`.
- Transformações de dados (ex.: normalizar nome/e-mail) ficam em `services/utils/*_data_formatter.py`.
- A camada `core/` nunca fala direto com o banco; usa sempre `database/queries/*`.
- Para novas features:
  - criar models em `database/models/`,
  - criar queries em `database/queries/`,
  - expor regras em `core/`,
  - criar schemas e routers em `interfaces/api/`.

