from html import escape
from urllib.parse import urljoin

from flask import current_app

from app.extension import db
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
from app.services.task_access_service import (
    issue_task_access_grant,
    revoke_active_task_grants
)

def build_absolute_url(
    relative_path: str,
) -> str:
    base_url = (
        current_app.config[
            "APP_BASE_URL"
        ].rstrip("/")
        + "/"
    )

    return urljoin(
        base_url,
        relative_path.lstrip("/"),
    )


def build_portal_task_url(
    task: WorkflowTask,
) -> str:
    """
    Build a portal-authenticated task URL.
    """

    if task.phase.is_final_approval:
        relative_path = (
            f"workflow/tasks/"
            f"{task.id}/approval"
        )
    else:
        relative_path = (
            f"workflow/tasks/{task.id}"
        )

    return build_absolute_url(
        relative_path
    )


def build_task_access_url(
    raw_token: str,
) -> str:
    """
    Build the secure departmental email link.
    """

    return build_absolute_url(
        f"task-access/{raw_token}"
    )

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
access_grant = None

department_name = (
    task.phase.department.name
    or ""
).strip().upper()

requires_portal_login = (
    task.phase.is_final_approval
    or department_name == "NOC"
)

if requires_portal_login:
    task_url = build_portal_task_url(
        task
    )

else:
    (
        access_grant,
        raw_token,
    ) = issue_task_access_grant(
        task=task,
        recipient_email=(
            notification.recipient_email
        ),
    )

    task_url = build_task_access_url(
        raw_token
    )

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
def create_overdue_task_notification(
    *,
    task: WorkflowTask,
    recipient_email: str,
    notification_type: str,
    deduplication_key: str,
) -> EmailNotification:
    """
    Create a persistent overdue-notification record.

    This function adds records to the current SQLAlchemy session
    but does not commit.
    """

    subject = (
        f"Overdue Offboarding Task — "
        f"{task.case.case_number} — "
        f"{task.phase.name}"
    )

    notification = EmailNotification(
        case=task.case,
        workflow_task=task,
        notification_type=notification_type,
        deduplication_key=deduplication_key,
        recipient_email=recipient_email,
        subject=subject,
        status="PENDING",
    )

    db.session.add(notification)

    db.session.add(
        AuditLog(
            case=task.case,
            action="OVERDUE_NOTIFICATION_QUEUED",
            performed_by="System",
            details=(
                f"An overdue escalation notification was queued "
                f"for workflow task {task.id}. "
                f"Notification type: {notification_type}. "
                f"Recipient: '{recipient_email}'."
            ),
        )
    )

    return notification


def deliver_overdue_task_notification(
    notification: EmailNotification,
) -> EmailResult:
    """
    Attempt delivery of an overdue-task escalation notification.

    The notification record and audit log are updated, but this
    function does not commit.
    """

    task = notification.workflow_task
    task_url = build_task_url(task)

    due_at_text = task.due_at.strftime(
        "%d %B %Y, %I:%M %p"
    )

    assigned_at_text = task.assigned_at.strftime(
        "%d %B %Y, %I:%M %p"
    )

    if task.opened_at is None:
        opened_status_text = "The task has not been opened."
    else:
        opened_status_text = (
            "The task was opened on "
            f"{task.opened_at.strftime('%d %B %Y, %I:%M %p')}, "
            "but it has not been submitted."
        )

    text_body = f"""
An employee offboarding task is overdue.

Case Number: {task.case.case_number}
Employee: {task.case.employee_name}
Phase: {task.phase.name}
Responsible Department: {task.phase.department.name}
Assigned Email: {task.assigned_to_email}
Task Status: {task.status}
Assigned At: {assigned_at_text}
Due At: {due_at_text}
Open Status: {opened_status_text}

Open the task:
{task_url}
""".strip()

    html_body = f"""
    <h2>Overdue Offboarding Task</h2>

    <p>
        An employee offboarding task has passed its due date
        and requires NOC attention.
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
            <strong>Responsible Department:</strong>
            {escape(task.phase.department.name)}
        </li>
        <li>
            <strong>Assigned Email:</strong>
            {escape(task.assigned_to_email)}
        </li>
        <li>
            <strong>Task Status:</strong>
            {escape(task.status)}
        </li>
        <li>
            <strong>Assigned At:</strong>
            {escape(assigned_at_text)}
        </li>
        <li>
            <strong>Due At:</strong>
            {escape(due_at_text)}
        </li>
        <li>
            <strong>Open Status:</strong>
            {escape(opened_status_text)}
        </li>
    </ul>

    <p>
        <a href="{escape(task_url)}">
            Open Overdue Task
        </a>
    </p>
    """.strip()

    notification.attempted_at = utc_now()
    notification.provider_message_id = None
    notification.error_message = None
    notification.sent_at = None

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

    notification.provider_message_id = (
        result.provider_message_id
    )

    notification.error_message = result.error_message

    if result.success:
        notification.status = "SENT"
        notification.sent_at = utc_now()

        action = "OVERDUE_NOTIFICATION_SENT"

        details = (
            f"Overdue escalation for workflow task {task.id} "
            f"was sent to '{notification.recipient_email}'."
        )

    else:
        notification.status = "FAILED"

        action = "OVERDUE_NOTIFICATION_FAILED"

        details = (
            f"Overdue escalation for workflow task {task.id} "
            f"failed for '{notification.recipient_email}'. "
            f"Reason: "
            f"{result.error_message or 'No reason returned.'}"
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