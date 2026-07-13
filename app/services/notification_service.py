from html import escape
from urllib.parse import urljoin

from flask import current_app

from app.extensions import db
from app.models import (
    AuditLog,
    EmailNotification,
    WorkflowTask,
    utc_now,
)
from app.services.email_service import (
    EmailResult,
    get_email_service,
)


def build_task_url(task: WorkflowTask) -> str:
    base_url = current_app.config["APP_BASE_URL"].rstrip("/") + "/"
    relative_path = f"workflow/tasks/{task.id}"

    return urljoin(base_url, relative_path)


def create_task_assignment_notification(
    task: WorkflowTask,
) -> EmailNotification:
    """
    Create a pending notification record.

    The notification is added to the current database session,
    but this function does not commit.
    """

    subject = (
        f"Offboarding Action Required — "
        f"{task.case.case_number}"
    )

    notification = EmailNotification(
        case=task.case,
        workflow_task=task,
        notification_type="TASK_ASSIGNED",
        recipient_email=task.assigned_to_email,
        subject=subject,
        status="PENDING",
    )

    db.session.add(notification)

    audit_log = AuditLog(
        case=task.case,
        action="TASK_NOTIFICATION_QUEUED",
        performed_by="System",
        details=(
            f"Task notification queued for "
            f"'{task.assigned_to_email}'."
        ),
    )

    db.session.add(audit_log)

    return notification


def deliver_task_assignment_notification(
    notification: EmailNotification,
) -> EmailResult:
    """
    Attempt delivery and update the notification record.

    This function changes the SQLAlchemy session but does not commit.
    """

    task = notification.workflow_task
    task_url = build_task_url(task)

    due_at_text = task.due_at.strftime(
        "%d %B %Y, %I:%M %p"
    )

    text_body = f"""
A new employee offboarding task has been assigned.

Case Number: {task.case.case_number}
Employee: {task.case.employee_name}
Phase: {task.phase.name}
Assigned Department: {task.phase.department.name}
Due At: {due_at_text}

Open the assigned task:
{task_url}
""".strip()

    html_body = f"""
    <h2>Offboarding Action Required</h2>

    <p>
        A new employee offboarding task has been assigned
        to your department.
    </p>

    <ul>
        <li>
            <strong>Case Number:</strong>
            {escape(task.case.case_number)}
        </li>
        <li>
            <strong>Employee:</strong>
            {escape(task.case.employee_name)}
        </li>
        <li>
            <strong>Phase:</strong>
            {escape(task.phase.name)}
        </li>
        <li>
            <strong>Assigned Department:</strong>
            {escape(task.phase.department.name)}
        </li>
        <li>
            <strong>Due At:</strong>
            {escape(due_at_text)}
        </li>
    </ul>

    <p>
        <a href="{escape(task_url)}">
            Open Assigned Task
        </a>
    </p>
    """.strip()

    notification.attempted_at = utc_now()

    try:
        email_service = get_email_service()

        result = email_service.send_email(
            recipients=[notification.recipient_email],
            subject=notification.subject,
            html_body=html_body,
            text_body=text_body,
        )

    except Exception as exc:
        result = EmailResult(
            success=False,
            error_message=str(exc),
        )

    notification.provider_message_id = result.provider_message_id
    notification.error_message = result.error_message

    if result.success:
        notification.status = "SENT"
        notification.sent_at = utc_now()

        action = "TASK_NOTIFICATION_SENT"
        details = (
            f"Task notification sent to "
            f"'{notification.recipient_email}'."
        )
    else:
        notification.status = "FAILED"

        action = "TASK_NOTIFICATION_FAILED"
        details = (
            f"Task notification failed for "
            f"'{notification.recipient_email}'. "
            f"Reason: {result.error_message}"
        )

    db.session.add(
        AuditLog(
            case=task.case,
            action=action,
            performed_by="System",
            details=details,
        )
    )

    return result