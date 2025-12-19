import os
import sys
from fastapi import APIRouter, Request, Header
from fastapi.responses import JSONResponse
from readme_metrics.VerifyWebhook import VerifyWebhook

# Verifica variável de ambiente obrigatória
if os.getenv("README_API_KEY") is None:
    sys.stderr.write("Missing `README_API_KEY` environment variable\n")
    sys.stderr.flush()
    sys.exit(1)

router = APIRouter()

# Ideal: usar variável de ambiente
README_WEBHOOK_SECRET = os.getenv(
    "README_WEBHOOK_SECRET",
    "hhQTlGP4uWDTBTJSe2XDljUcceqdK3Z1",  # fallback (não recomendado em prod)
)


@router.post("/")
async def webhook(
    request: Request,
    readme_signature: str | None = Header(default=None, alias="readme-signature"),
):
    body = await request.json()

    try:
        # Verifica se a requisição veio do ReadMe
        VerifyWebhook(body, readme_signature, README_WEBHOOK_SECRET)
    except Exception as error:
        return JSONResponse(
            content={"error": str(error)},
            status_code=401,
        )
    # Aqui você pode buscar dados do usuário e retornar variáveis dinâmicas
    return JSONResponse(
        content={
            "message": "Webhook received",
        },
        status_code=200,
    )
