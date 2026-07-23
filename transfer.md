import smtplib
import ssl
from email.message import EmailMessage


MX_HOST = "YOUR-MAIL-EXCHANGER.mail.protection.outlook.com"
INTERN_EMAIL = "your.intern.address@company.com"


message = EmailMessage()
message["From"] = INTERN_EMAIL
message["To"] = INTERN_EMAIL
message["Subject"] = "Offboarding workflow Direct Send test"

message.set_content(
    "This is a controlled SMTP Direct Send test for the "
    "offboarding workflow prototype."
)


try:
    with smtplib.SMTP(
        host=MX_HOST,
        port=25,
        timeout=20,
    ) as smtp:
        smtp.ehlo()

        if smtp.has_extn("STARTTLS"):
            smtp.starttls(
                context=ssl.create_default_context()
            )
            smtp.ehlo()

        refused_recipients = smtp.send_message(message)

        if refused_recipients:
            print(
                "The SMTP server refused one or more recipients:",
                refused_recipients,
            )
        else:
            print(
                "The SMTP server accepted the message for delivery."
            )

except smtplib.SMTPResponseException as exc:
    error_message = exc.smtp_error

    if isinstance(error_message, bytes):
        error_message = error_message.decode(
            errors="replace"
        )

    print(
        f"SMTP rejected the request: "
        f"{exc.smtp_code} {error_message}"
    )

except Exception as exc:
    print(
        f"SMTP test failed: "
        f"{type(exc).__name__}: {exc}"
    )