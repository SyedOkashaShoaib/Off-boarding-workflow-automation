from html import escape
from urllib.parse import urlencode, urljoin

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
    revoke_grant,
)


# ============================================================
# URL construction
# ============================================================

def build_absolute_url(
    relative_path: str,
) -> str:
    """
    Convert an application-relative path into a complete URL.

    APP_BASE_URL must contain the externally reachable application
    address in production.
    """

    base_url = (
        current_app.config[
            "APP_BASE_URL"
        ].rstrip("/")
        + "/"
    )

    return urljoin(
        base_url,
        str(relative_path).lstrip("/"),
    )


def build_portal_task_url(
    task: WorkflowTask,
) -> str:
    """
    Build a task URL that requires authenticated portal access.

    NOC checklist tasks use the departmental task route.
    Final Admin tasks use the dedicated approval route.
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
    Build the secure bearer-token URL sent to MIS and Hardware.
    """

    return build_absolute_url(
        f"task-access/{raw_token}"
    )


def build_case_register_url(
    task: WorkflowTask,
) -> str:
    """
    Build an authenticated Cases-register URL for NOC monitoring.

    This is used for overdue escalations. It does not provide NOC
    with a departmental task-access token.
    """

    query_string = urlencode(
        {
            "status": "all",
            "q": task.case.case_number,
        }
    )

    return build_absolute_url(
        f"cases/?{query_string}"
    )


# ============================================================
# Shared helpers
# ============================================================

def task_requires_portal_login(
    task: WorkflowTask,
) -> bool:
    """
    Return whether the assignment must use portal authentication.

    NOC users and final approvers use authenticated portal access.
    Other departmental users receive task-specific access grants.
    """

    department_name = str(
        task.phase.department.name or ""
    ).strip().upper()

    return bool(
        task.phase.is_final_approval
        or department_name == "NOC"
    )


def format_datetime(
    value,
) -> str:
    """
    Format an application datetime for notification messages.
    """

    if value is None:
        return "Not recorded"

    return value.strftime(
        "%d %B %Y, %I:%M %p"
    )


def send_notification_email(
    *,
    notification: EmailNotification,
    html_body: str,
    text_body: str,
) -> EmailResult:
    """
    Send one notification through the configured email backend.

    Backend exceptions are converted into an EmailResult so the
    notification record can still be marked as failed.
    """

    try:
        email_service = get_email_service()

        return email_service.send_email(
            recipients=[
                notification.recipient_email
            ],
            subject=notification.subject,
            html_body=html_body,
            text_body=text_body,
        )

    except Exception as exc:
        current_app.logger.exception(
            (
                "Unexpected error while sending email "
                "notification %s."
            ),
            notification.id,
        )

        return EmailResult(
            success=False,
            error_message=str(exc),
        )


# ============================================================
# Assignment notifications
# ============================================================

def create_task_assignment_notification(
    task: WorkflowTask,
) -> EmailNotification:
    """
    Create a pending task-assignment notification.

    This function adds records to the active SQLAlchemy session but
    does not commit. The calling workflow controls the transaction.
    """

    subject = (
        "Offboarding Action Required — "
        f"{task.case.case_number}"
    )

    notification = EmailNotification(
        case=task.case,
        workflow_task=task,
        notification_type="TASK_ASSIGNED",
        recipient_email=(
            task.assigned_to_email
        ),
        subject=subject,
        status="PENDING",
    )

    db.session.add(notification)

    db.session.add(
        AuditLog(
            case=task.case,
            action=(
                "TASK_NOTIFICATION_QUEUED"
            ),
            performed_by="System",
            details=(
                "Task notification queued for "
                f"'{task.assigned_to_email}'."
            ),
        )
    )

    return notification


def deliver_task_assignment_notification(
    notification: EmailNotification,
) -> EmailResult:
    """
    Attempt delivery of a task-assignment notification.

    NOC and final Admin tasks receive portal-authenticated links.
    MIS and Hardware tasks receive secure task-specific access links.

    This function updates the current SQLAlchemy session but does not
    commit. The calling workflow remains responsible for committing.
    """

    task = notification.workflow_task
    access_grant = None

    notification.attempted_at = utc_now()
    notification.provider_message_id = None
    notification.error_message = None
    notification.sent_at = None

    try:
        requires_portal_login = (
            task_requires_portal_login(
                task
            )
        )

        if requires_portal_login:
            task_url = (
                build_portal_task_url(
                    task
                )
            )

            security_notice = (
                "Sign in through the authorised "
                "offboarding operations portal to "
                "open this assignment."
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

            task_url = (
                build_task_access_url(
                    raw_token
                )
            )

            security_notice = (
                "This secure link is intended only "
                "for the assigned department. "
                "Do not forward it."
            )

        due_at_text = format_datetime(
            task.due_at
        )

        text_body = f"""
A new employee offboarding task has been assigned.

Case Number: {task.case.case_number}
Employee: {task.case.employee_name}
Employee ID: {task.case.employee_id}
Phase: {task.phase.name}
Assigned Department: {task.phase.department.name}
Due At: {due_at_text}

Open the assigned task:
{task_url}

Security notice:
{security_notice}
""".strip()

        html_body = f"""
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>
        {escape(notification.subject)}
    </title>
</head>

<body>
    <h1>Offboarding Action Required</h1>

    <p>
        A new employee offboarding task has been assigned.
    </p>

    <table
        role="presentation"
        cellpadding="6"
        cellspacing="0"
        border="0"
    >
        <tr>
            <th align="left">Case Number</th>
            <td>
                {escape(task.case.case_number)}
            </td>
        </tr>

        <tr>
            <th align="left">Employee</th>
            <td>
                {escape(task.case.employee_name)}
            </td>
        </tr>

        <tr>
            <th align="left">Employee ID</th>
            <td>
                {escape(task.case.employee_id)}
            </td>
        </tr>

        <tr>
            <th align="left">Phase</th>
            <td>
                {escape(task.phase.name)}
            </td>
        </tr>

        <tr>
            <th align="left">
                Assigned Department
            </th>
            <td>
                {
                    escape(
                        task.phase.department.name
                    )
                }
            </td>
        </tr>

        <tr>
            <th align="left">Due At</th>
            <td>
                {escape(due_at_text)}
            </td>
        </tr>
    </table>

    <p>
        <strong>Security notice:</strong>
        {escape(security_notice)}
    </p>

    <p>
        <a href="{escape(task_url)}">
            Open Assigned Task
        </a>
    </p>
</body>
</html>
""".strip()

        result = send_notification_email(
            notification=notification,
            html_body=html_body,
            text_body=text_body,
        )

    except Exception as exc:
        current_app.logger.exception(
            (
                "Could not prepare task assignment "
                "notification %s."
            ),
            notification.id,
        )

        result = EmailResult(
            success=False,
            error_message=str(exc),
        )

    notification.provider_message_id = (
        result.provider_message_id
    )

    notification.error_message = (
        result.error_message
    )

    if result.success:
        notification.status = "SENT"
        notification.sent_at = utc_now()
        notification.error_message = None

        action = "TASK_NOTIFICATION_SENT"

        details = (
            "Task notification sent to "
            f"'{notification.recipient_email}'."
        )

    else:
        notification.status = "FAILED"
        notification.sent_at = None

        if access_grant is not None:
            revoke_grant(
                access_grant
            )

        action = "TASK_NOTIFICATION_FAILED"

        details = (
            "Task notification failed for "
            f"'{notification.recipient_email}'. "
            "Reason: "
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


# ============================================================
# Overdue escalation notifications
# ============================================================

def create_overdue_task_notification(
    *,
    task: WorkflowTask,
    recipient_email: str,
    notification_type: str,
    deduplication_key: str,
) -> EmailNotification:
    """
    Create a persistent overdue escalation notification.

    This function adds records to the active SQLAlchemy session but
    does not commit.
    """

    subject = (
        "Overdue Offboarding Task — "
        f"{task.case.case_number} — "
        f"{task.phase.name}"
    )

    notification = EmailNotification(
        case=task.case,
        workflow_task=task,
        notification_type=(
            notification_type
        ),
        deduplication_key=(
            deduplication_key
        ),
        recipient_email=(
            recipient_email
        ),
        subject=subject,
        status="PENDING",
    )

    db.session.add(notification)

    db.session.add(
        AuditLog(
            case=task.case,
            action=(
                "OVERDUE_NOTIFICATION_QUEUED"
            ),
            performed_by="System",
            details=(
                "An overdue escalation notification "
                f"was queued for workflow task {task.id}. "
                "Notification type: "
                f"{notification_type}. "
                "Recipient: "
                f"'{recipient_email}'."
            ),
        )
    )

    return notification


def deliver_overdue_task_notification(
    notification: EmailNotification,
) -> EmailResult:
    """
    Attempt delivery of an overdue-task escalation.

    Overdue escalation recipients are directed to the authenticated
    Cases register. They are not issued departmental task tokens.

    This function updates the current SQLAlchemy session but does not
    commit.
    """

    task = notification.workflow_task

    notification.attempted_at = utc_now()
    notification.provider_message_id = None
    notification.error_message = None
    notification.sent_at = None

    case_register_url = (
        build_case_register_url(
            task
        )
    )

    due_at_text = format_datetime(
        task.due_at
    )

    assigned_at_text = format_datetime(
        task.assigned_at
    )

    if task.opened_at is None:
        opened_status_text = (
            "The task has not been opened."
        )
    else:
        opened_status_text = (
            "The task was opened on "
            f"{format_datetime(task.opened_at)}, "
            "but it has not been submitted."
        )

    text_body = f"""
An employee offboarding task is overdue.

Case Number: {task.case.case_number}
Employee: {task.case.employee_name}
Employee ID: {task.case.employee_id}
Phase: {task.phase.name}
Responsible Department: {task.phase.department.name}
Assigned Email: {task.assigned_to_email}
Task Status: {task.status}
Assigned At: {assigned_at_text}
Due At: {due_at_text}
Open Status: {opened_status_text}

Review the case in the authenticated portal:
{case_register_url}
""".strip()

    html_body = f"""
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>
        {escape(notification.subject)}
    </title>
</head>

<body>
    <h1>Overdue Offboarding Task</h1>

    <p>
        An employee offboarding task has passed its due
        date and requires NOC attention.
    </p>

    <table
        role="presentation"
        cellpadding="6"
        cellspacing="0"
        border="0"
    >
        <tr>
            <th align="left">Case Number</th>
            <td>
                {escape(task.case.case_number)}
            </td>
        </tr>

        <tr>
            <th align="left">Employee</th>
            <td>
                {escape(task.case.employee_name)}
            </td>
        </tr>

        <tr>
            <th align="left">Employee ID</th>
            <td>
                {escape(task.case.employee_id)}
            </td>
        </tr>

        <tr>
            <th align="left">Phase</th>
            <td>
                {escape(task.phase.name)}
            </td>
        </tr>

        <tr>
            <th align="left">
                Responsible Department
            </th>
            <td>
                {
                    escape(
                        task.phase.department.name
                    )
                }
            </td>
        </tr>

        <tr>
            <th align="left">
                Assigned Email
            </th>
            <td>
                {escape(task.assigned_to_email)}
            </td>
        </tr>

        <tr>
            <th align="left">Task Status</th>
            <td>
                {escape(task.status)}
            </td>
        </tr>

        <tr>
            <th align="left">Assigned At</th>
            <td>
                {escape(assigned_at_text)}
            </td>
        </tr>

        <tr>
            <th align="left">Due At</th>
            <td>
                {escape(due_at_text)}
            </td>
        </tr>

        <tr>
            <th align="left">Open Status</th>
            <td>
                {escape(opened_status_text)}
            </td>
        </tr>
    </table>

    <p>
        <a href="{escape(case_register_url)}">
            Review Case in Portal
        </a>
    </p>
</body>
</html>
""".strip()

    result = send_notification_email(
        notification=notification,
        html_body=html_body,
        text_body=text_body,
    )

    notification.provider_message_id = (
        result.provider_message_id
    )

    notification.error_message = (
        result.error_message
    )

    if result.success:
        notification.status = "SENT"
        notification.sent_at = utc_now()
        notification.error_message = None

        action = (
            "OVERDUE_NOTIFICATION_SENT"
        )

        details = (
            "Overdue escalation for workflow task "
            f"{task.id} was sent to "
            f"'{notification.recipient_email}'."
        )

    else:
        notification.status = "FAILED"
        notification.sent_at = None

        action = (
            "OVERDUE_NOTIFICATION_FAILED"
        )

        details = (
            "Overdue escalation for workflow task "
            f"{task.id} failed for "
            f"'{notification.recipient_email}'. "
            "Reason: "
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