import os
from dotenv import load_dotenv


class Settings:
    load_dotenv()

    # Security
    SECRET: str = os.environ.get("SECRET")

    # Environment
    ENVIRONMENT: str = os.environ.get("ENVIRONMENT", "development")

    # DB Config (production)
    PRIME_DB_URL: str = os.environ.get("PRIME_DB_URL")
    DB_NAME: str = os.environ.get("DB_NAME")
    DB_USER: str = os.environ.get("DB_USER")
    DB_PWD: str = os.environ.get("DB_PWD")
    DB_HOST: str = os.environ.get("DB_HOST")
    DB_PORT: str = os.environ.get("DB_PORT")

    # DB Config (local SQLite)
    SQLITE_DB_URL: str = os.environ.get("SQLITE_DB_URL", "sqlite:///./pad_local.db")

    # GCP Config
    GOOGLE_APPLICATION_CREDENTIALS: str = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    GAE_APPLICATION: str = os.environ.get("GAE_APPLICATION")

    # Main Config
    API_HOST: str = os.environ.get("API_HOST")
    LOG_LEVEL: str = os.environ.get("LOG_LEVEL", "debug")
    RELOAD: str = os.environ.get("RELOAD")


settings = Settings()