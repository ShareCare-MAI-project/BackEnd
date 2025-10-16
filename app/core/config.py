import os

SECRET_KEY = os.getenv("SECRET_KEY", "fake_key")
DATABASE_URL = os.getenv("DATABASE_URL", "fake_db")

PROJECT_NAME = "ShareCare API"
