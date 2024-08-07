import os

DATABASE_URL = (
    os.getenv("DATABASE_URL") or "postgresql+asyncpg://user:password@db:5432/mydatabase"
)
USE_POSTGRES = os.getenv("USE_POSTGRES", "False") == "True"

EMAIL_HOST = os.getenv("EMAIL_HOST", "localhost")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", 587))
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", "user")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", "password")
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", "True") == "True"
EMAIL_FROM = os.getenv("EMAIL_FROM", "celery@localhost")
