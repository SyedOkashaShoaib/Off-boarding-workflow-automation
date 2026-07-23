SMTP_HOST = os.environ.get(
    "SMTP_HOST",
    "",
).strip()

SMTP_PORT = environment_positive_integer(
    "SMTP_PORT",
    default=25,
)

SMTP_TIMEOUT_SECONDS = environment_positive_integer(
    "SMTP_TIMEOUT_SECONDS",
    default=20,
)

SMTP_SENDER_ADDRESS = os.environ.get(
    "SMTP_SENDER_ADDRESS",
    "",
).strip().lower()

SMTP_ALLOWED_RECIPIENT = os.environ.get(
    "SMTP_ALLOWED_RECIPIENT",
    "",
).strip().lower()

SMTP_USE_STARTTLS = environment_flag(
    "SMTP_USE_STARTTLS",
    default=False,
)

SMTP_ALLOW_PLAINTEXT = environment_flag(
    "SMTP_ALLOW_PLAINTEXT",
    default=False,
)