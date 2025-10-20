import os

SECRET_KEY = os.getenv("SECRET_KEY", "fake_key")
DATABASE_URL = os.getenv("DATABASE_URL", "fake_db")

FERNET_KEY = os.getenv("FERNET_KEY", "fApsNI6yQf9_LLLkwRH0BYNa3Y64WvIb-b6xofLG4PU=")

PROJECT_NAME = "ShareCare API"

HOST = "0.0.0.0"
PORT = 8000
