Instruções para baixar o repositório

Ao clonar o REPO criar um arquivo chamado .env e incluir as seguintes variaveis

## Aplication Config
export API_HOST = "127.0.0.1"
export API_PORT = 8000
export LOG_LEVEL = "info"
export RELOAD = True
export WORKERS = 1

## Desenvolvimento
export PRIME_DB_URL='mysql://root:"suasenharoot"@127.0.0.1:3306/pad_teste'
export DB_NAME="pad_teste"
export DB_USER="root"
export DB_PWD="suasenharoot"
export DB_HOST="127.0.0.1"
export DB_PORT="3306"

