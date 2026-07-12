from abc import ABC, abstractmethod
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Optional

from flask import current_app


@dataclass(frozen=True)
class EmailResult:
    success: bool
    provider_message_id: Optional[str] = None
    error_message: Optional[str] = None


class EmailService(ABC):
    @abstractmethod
    def send_email(
        self,
        *,
        recipients: Sequence[str],
        subject: str,
        html_body: str,
        text_body: Optional[str] = None,
    ) -> EmailResult:
        raise NotImplementedError


class ConsoleEmailService(EmailService):
    def send_email(
        self,
        *,
        recipients: Sequence[str],
        subject: str,
        html_body: str,
        text_body: Optional[str] = None,
    ) -> EmailResult:
        recipient_list = [
            address.strip()
            for address in recipients
            if address and address.strip()
        ]

        if not recipient_list:
            return EmailResult(
                success=False,
                error_message="At least one recipient email address is required.",
            )

        print("\n" + "=" * 70)
        print("EMAIL NOTIFICATION — DEVELOPMENT MODE")
        print("=" * 70)
        print(f"To: {', '.join(recipient_list)}")
        print(f"Subject: {subject}")
        print("-" * 70)

        if text_body:
            print(text_body)
        else:
            print(html_body)

        print("=" * 70 + "\n")

        return EmailResult(
            success=True,
            provider_message_id="console-development-email",
        )


def create_email_service(backend_name: str) -> EmailService:
    normalized_backend = backend_name.strip().lower()

    if normalized_backend == "console":
        return ConsoleEmailService()

    raise ValueError(
        f"Unsupported email backend: {backend_name}"
    )


def get_email_service() -> EmailService:

    backend_name = current_app.config.get(
        "EMAIL_BACKEND",
        "console",
    )

    return create_email_service(backend_name)