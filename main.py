"""Main file"""
import argparse

import uvicorn
from fastapi import FastAPI

from services.config import settings
from interfaces.api.config import create_app


# Instância global da aplicação FastAPI
# (usada tanto pelo uvicorn.run quanto por comandos como `uvicorn main:app`)
app: FastAPI = create_app()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PrimeAutoDocs")
    parser.add_argument(
        "--mode",
        choices=["api", "cli"],
        default="api",
        help="Execution mode(api or cli)",
    )

    args = parser.parse_args()

    if args.mode == "api":
        uvicorn.run(
            "main:app",
            host=settings.API_HOST,
            port=8000,
            log_level=settings.LOG_LEVEL,
            reload=settings.RELOAD,
            workers=1,
        )

    elif args.mode == "cli":
        print("Unauthorized")