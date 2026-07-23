from abc import ABC, abstractmethod
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from email.message import EmailMessage
from email.utils import make_msgid, parseaddr
import smtplib
import socket
import ssl
from typing import Optional

from flask import current_app


@dataclass(frozen=True)
class EmailResult:
    """
    Outcome returned by an email transport provider.

    A successful result means that the SMTP provider accepted the
    message for processing. It does not independently confirm inbox
    delivery.
    """

    success: bool
    provider_message_id: Optional[str] = None
    error_message: Optional[str] = None


class EmailService(ABC):
    """
    Provider-independent interface used by workflow notifications.
    """

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
    """
    Development provider that prints email content to the console.
    """

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
                error_message=(
                    "At least one recipient email address is required."
                ),
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
            provider_message_id=(
                "console-development-email"
            ),
        )


class SmtpDirectSendEmailService(EmailService):
    """
    Microsoft 365 Direct Send provider for the controlled prototype.

    The provider permits delivery only to one configured internal
    mailbox. It does not authenticate as that mailbox and does not
    store an Outlook password.
    """

    def __init__(
        self,
        *,
        host: str,
        port: int,
        sender_address: str,
        allowed_recipient: str,
        timeout_seconds: int,
        use_starttls: bool,
        allow_plaintext: bool,
    ) -> None:
        self.host = str(host or "").strip()
        self.port = int(port)
        self.sender_address = self._normalize_address(
            sender_address
        )
        self.allowed_recipient = self._normalize_address(
            allowed_recipient
        )
        self.timeout_seconds = int(timeout_seconds)
        self.use_starttls = bool(use_starttls)
        self.allow_plaintext = bool(allow_plaintext)

        self._validate_configuration()

    @staticmethod
    def _normalize_address(
        address: str,
    ) -> str:
        """
        Extract and normalize the email address portion of a value.
        """

        _, parsed_address = parseaddr(
            str(address or "").strip()
        )

        return parsed_address.strip().lower()

    def _validate_configuration(self) -> None:
        if not self.host:
            raise ValueError(
                "SMTP_HOST must be configured for "
                "the smtp_direct email backend."
            )

        if self.port < 1:
            raise ValueError(
                "SMTP_PORT must be a positive integer."
            )

        if self.timeout_seconds < 1:
            raise ValueError(
                "SMTP_TIMEOUT_SECONDS must be positive."
            )

        if not self.sender_address:
            raise ValueError(
                "SMTP_SENDER_ADDRESS must contain "
                "a valid email address."
            )

        if not self.allowed_recipient:
            raise ValueError(
                "SMTP_ALLOWED_RECIPIENT must contain "
                "a valid email address."
            )

        if (
            not self.use_starttls
            and not self.allow_plaintext
        ):
            raise ValueError(
                "Plaintext SMTP transport is disabled. "
                "Set SMTP_ALLOW_PLAINTEXT=true only for "
                "the approved prototype environment."
            )

    def _prepare_recipients(
        self,
        recipients: Sequence[str],
    ) -> list[str]:
        """
        Normalize recipients and enforce the prototype allowlist.
        """

        normalized_recipients = []
        seen_addresses = set()

        for recipient in recipients:
            normalized_address = self._normalize_address(
                recipient
            )

            if (
                normalized_address
                and normalized_address
                not in seen_addresses
            ):
                normalized_recipients.append(
                    normalized_address
                )
                seen_addresses.add(
                    normalized_address
                )

        if not normalized_recipients:
            raise ValueError(
                "At least one recipient email address is required."
            )

        unauthorized_recipients = [
            recipient
            for recipient in normalized_recipients
            if recipient != self.allowed_recipient
        ]

        if unauthorized_recipients:
            raise ValueError(
                "SMTP Direct Send refused a recipient "
                "that is not the configured prototype mailbox."
            )

        return normalized_recipients

    def _build_message(
        self,
        *,
        recipients: Sequence[str],
        subject: str,
        html_body: str,
        text_body: Optional[str],
    ) -> tuple[EmailMessage, str]:
        normalized_subject = str(
            subject or ""
        ).strip()

        if not normalized_subject:
            raise ValueError(
                "Email subject is required."
            )

        normalized_html_body = str(
            html_body or ""
        ).strip()

        normalized_text_body = str(
            text_body or ""
        ).strip()

        if (
            not normalized_html_body
            and not normalized_text_body
        ):
            raise ValueError(
                "Email body content is required."
            )

        sender_domain = self.sender_address.partition(
            "@"
        )[2]

        message_id = make_msgid(
            domain=sender_domain or None
        )

        message = EmailMessage()
        message["Message-ID"] = message_id
        message["From"] = self.sender_address
        message["To"] = ", ".join(recipients)
        message["Subject"] = normalized_subject

        if normalized_text_body:
            message.set_content(
                normalized_text_body
            )
        else:
            message.set_content(
                "This notification contains an HTML version."
            )

        if normalized_html_body:
            message.add_alternative(
                normalized_html_body,
                subtype="html",
            )

        return message, message_id

    def send_email(
        self,
        *,
        recipients: Sequence[str],
        subject: str,
        html_body: str,
        text_body: Optional[str] = None,
    ) -> EmailResult:
        """
        Submit one message through the configured MX endpoint.
        """

        try:
            recipient_list = self._prepare_recipients(
                recipients
            )

            message, message_id = self._build_message(
                recipients=recipient_list,
                subject=subject,
                html_body=html_body,
                text_body=text_body,
            )

            with smtplib.SMTP(
                host=self.host,
                port=self.port,
                timeout=self.timeout_seconds,
            ) as smtp:
                smtp.ehlo_or_helo_if_needed()

                if self.use_starttls:
                    if not smtp.has_extn("STARTTLS"):
                        return EmailResult(
                            success=False,
                            error_message=(
                                "The SMTP endpoint did not "
                                "advertise STARTTLS."
                            ),
                        )

                    smtp.starttls(
                        context=ssl.create_default_context()
                    )

                    smtp.ehlo()

                refused_recipients = smtp.send_message(
                    message,
                    from_addr=self.sender_address,
                    to_addrs=recipient_list,
                )

            if refused_recipients:
                return EmailResult(
                    success=False,
                    error_message=(
                        "The SMTP server refused one or more "
                        "configured recipients."
                    ),
                )

            return EmailResult(
                success=True,
                provider_message_id=message_id,
            )

        except ValueError as exc:
            return EmailResult(
                success=False,
                error_message=str(exc),
            )

        except smtplib.SMTPRecipientsRefused:
            return EmailResult(
                success=False,
                error_message=(
                    "The SMTP server rejected the recipient."
                ),
            )

        except smtplib.SMTPSenderRefused as exc:
            return EmailResult(
                success=False,
                error_message=(
                    "The SMTP server rejected the sender "
                    f"with response code {exc.smtp_code}."
                ),
            )

        except smtplib.SMTPResponseException as exc:
            return EmailResult(
                success=False,
                error_message=(
                    "The SMTP server rejected the message "
                    f"with response code {exc.smtp_code}."
                ),
            )

        except smtplib.SMTPException as exc:
            return EmailResult(
                success=False,
                error_message=(
                    "An SMTP protocol error occurred: "
                    f"{type(exc).__name__}."
                ),
            )

        except socket.timeout:
            return EmailResult(
                success=False,
                error_message=(
                    "The SMTP connection timed out."
                ),
            )

        except ssl.SSLError:
            return EmailResult(
                success=False,
                error_message=(
                    "The SMTP TLS connection could not "
                    "be established securely."
                ),
            )

        except OSError as exc:
            return EmailResult(
                success=False,
                error_message=(
                    "The SMTP endpoint could not be reached: "
                    f"{type(exc).__name__}."
                ),
            )


def create_email_service(
    backend_name: str,
    config: Optional[Mapping] = None,
) -> EmailService:
    """
    Construct the configured email transport provider.
    """

    normalized_backend = str(
        backend_name or ""
    ).strip().lower()

    if normalized_backend == "console":
        return ConsoleEmailService()

    if normalized_backend == "smtp_direct":
        if config is None:
            raise ValueError(
                "Application configuration is required "
                "for the smtp_direct backend."
            )

        return SmtpDirectSendEmailService(
            host=config.get(
                "SMTP_HOST",
                "",
            ),
            port=config.get(
                "SMTP_PORT",
                25,
            ),
            sender_address=config.get(
                "SMTP_SENDER_ADDRESS",
                "",
            ),
            allowed_recipient=config.get(
                "SMTP_ALLOWED_RECIPIENT",
                "",
            ),
            timeout_seconds=config.get(
                "SMTP_TIMEOUT_SECONDS",
                20,
            ),
            use_starttls=config.get(
                "SMTP_USE_STARTTLS",
                False,
            ),
            allow_plaintext=config.get(
                "SMTP_ALLOW_PLAINTEXT",
                False,
            ),
        )

    raise ValueError(
        f"Unsupported email backend: {backend_name}"
    )


def get_email_service() -> EmailService:
    """
    Return the provider selected by the active Flask application.
    """

    backend_name = current_app.config.get(
        "EMAIL_BACKEND",
        "console",
    )

    return create_email_service(
        backend_name,
        current_app.config,
    )