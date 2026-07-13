from html import escape
from urllib.parse import urljoin

from flask import current_app

from app.models import WorkflowTask
from app.services.email_service import (
    EmailResult,
    get_email_service,
)


def build_task_url(task: WorkflowTask) -> str:
    """
    Build the absolute URL that the assigned department will open.
    """

    base_url = current_app.config["APP_BASE_URL"].rstrip("/") + "/"
    relative_path = f"workflow/tasks/{task.id}"

    return urljoin(base_url, relative_path)


def send_task_assignment_notification(
    task: WorkflowTask,
) -> EmailResult:
    """
    Build and send an offboarding task-assignment email.
    """

    email_service = get_email_service()
    task_url = build_task_url(task)

    due_at_text = task.due_at.strftime(
        "%d %B %Y, %I:%M %p"
    )

    subject = (
        f"Offboarding Action Required — "
        f"{task.case.case_number}"
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

    return email_service.send_email(
        recipients=[task.assigned_to_email],
        subject=subject,
        html_body=html_body,
        text_body=text_body,
    )












