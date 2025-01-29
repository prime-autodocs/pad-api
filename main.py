import argparse

import uvicorn
from services.config import settings

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
            "interfaces.api.config:app",
            host=settings.API_HOST,
            port=settings.API_PORT,
            log_level=settings.LOG_LEVEL,
            reload=settings.RELOAD,
            workers=settings.WORKERS
        )
    
    elif args.mode == "cli":
        print("Unauthorized")