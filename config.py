import os
from datetime import timedelta

from dotenv import load_dotenv


load_dotenv()


def environment_flag(
    name: str,
    default: bool = False,
) -> bool:
    """
    Parse a boolean environment variable safely.
    """

    raw_value = os.environ.get(name)

    if raw_value is None:
        return default

    return raw_value.strip().lower() in {
        "1",
        "true",
        "yes",
        "on",
    }

def environment_positive_integer(
    name: str,
    default: int,
) -> int:
    """
    Parse a positive integer environment variable safely.
    """

    raw_value = os.environ.get(name)

    if raw_value is None:
        return default

    try:
        parsed_value = int(raw_value)
    except (TypeError, ValueError):
        return default

    if parsed_value < 1:
        return default

    return parsed_value

class Config:
    SECRET_KEY = os.environ.get(
        "SECRET_KEY"
    )

    if not SECRET_KEY:
        raise RuntimeError(
            "SECRET_KEY must be configured in the environment."
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
    SMTP_HOST = os.environ.get( "SMTP_HOST", "", ).strip()

    SMTP_PORT = environment_positive_integer( "SMTP_PORT", default=25, )

    SMTP_TIMEOUT_SECONDS = environment_positive_integer( "SMTP_TIMEOUT_SECONDS", default=20, )

    SMTP_SENDER_ADDRESS = os.environ.get( "SMTP_SENDER_ADDRESS", "", ).strip().lower()

    SMTP_ALLOWED_RECIPIENT = os.environ.get( "SMTP_ALLOWED_RECIPIENT", "", ).strip().lower()

    SMTP_USE_STARTTLS = environment_flag( "SMTP_USE_STARTTLS", default=False, )

    SMTP_ALLOW_PLAINTEXT = environment_flag( "SMTP_ALLOW_PLAINTEXT", default=False, )
    APP_BASE_URL = os.environ.get(
        "APP_BASE_URL",
        "http://127.0.0.1:5000",
    )

    ENVIRONMENT_LABEL = os.environ.get(
        "ENVIRONMENT_LABEL",
        "Development",
    )
    TASK_ACCESS_TOKEN_LIFETIME_HOURS= (
        environment_positive_integer(
            "TASK_ACCESS_TOKEN_LIFETIME_HOURS",
            default=336, #14 days. 
        )
    )
    FINAL_APPROVAL_TOKEN_LIFETIME_HOURS = (
    environment_positive_integer(
        "FINAL_APPROVAL_TOKEN_LIFETIME_HOURS",
        default=336,
    )
)
    # Session cookie cannot be accessed through JavaScript.
    SESSION_COOKIE_HTTPONLY = True

    # Appropriate default for a conventional internal application.
    SESSION_COOKIE_SAMESITE = "Lax"

    # False for local HTTP development; must be true behind
    # production HTTPS.
    SESSION_COOKIE_SECURE = environment_flag(
        "SESSION_COOKIE_SECURE",
        default=False,
    )

    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_SAMESITE = "Lax"

    REMEMBER_COOKIE_SECURE = environment_flag(
        "SESSION_COOKIE_SECURE",
        default=False,
    )

    PERMANENT_SESSION_LIFETIME = timedelta(
        hours=8
    )

