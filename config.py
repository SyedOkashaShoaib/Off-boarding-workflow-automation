import os

from dotenv import load_dotenv


load_dotenv()


class Config:
    SECRET_KEY = os.environ.get(
        "SECRET_KEY",
        "development-secret-key",
    )

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "sqlite:///offboarding.db",
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    EMAIL_BACKEND = os.environ.get(
        "EMAIL_BACKEND",
        "console",
    )

    APP_BASE_URL = os.environ.get(
        "APP_BASE_URL",
        "http://127.0.0.1:5000",
    )

    ENVIRONMENT_LABEL = os.getenv(
        "ENVIRONMENT_LABEL",
        "Development"
    )