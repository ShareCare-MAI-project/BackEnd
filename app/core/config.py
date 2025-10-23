import os

PROJECT_NAME = "ShareCare API"

POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "fake_password")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_USER = os.getenv("POSTGRES_USER", "user")
POSTGRES_DB = os.getenv("POSTGRES_DB", "sharecare")

FERNET_KEY = os.getenv("ENCRYPTION_KEY", "fApsNI6yQf9_LLLkwRH0BYNa3Y64WvIb-b6xofLG4PU=")

SERVER_PORT = int(os.getenv("SERVER_PORT", 8000))
