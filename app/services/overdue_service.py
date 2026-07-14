from datetime import date

from flask import current_app

from app.models import (
    Department,
    EmailNotification,
    OffboardingCase,
    WorkflowTask,
    utc_now,
)


OPEN_TASK_STATUSES = (
    "PENDING",
    "IN_PROGRESS",
)


class OverdueConfigurationError(Exception):
    """Raised when overdue escalation cannot be configured safely."""


def find_overdue_tasks(
    task_id: int | None = None,
) -> list[WorkflowTask]:
    """
    Return active tasks whose due date has passed.

    Closed cases and completed tasks are excluded.
    """

    query = (
        WorkflowTask.query
        .join(
            OffboardingCase,
            WorkflowTask.case_id == OffboardingCase.id,
        )
        .filter(
            WorkflowTask.status.in_(OPEN_TASK_STATUSES),
            WorkflowTask.due_at <= utc_now(),
            OffboardingCase.status != "CLOSED",
        )
        .order_by(
            WorkflowTask.due_at.asc(),
            WorkflowTask.id.asc(),
        )
    )

    if task_id is not None:
        query = query.filter(
            WorkflowTask.id == task_id
        )

    return query.all()


def get_escalation_recipient_email() -> str:
    """
    Return the configured escalation department's email address.
    """

    department_name = current_app.config.get(
        "OVERDUE_ESCALATION_DEPARTMENT",
        "NOC",
    )

    department = Department.query.filter_by(
        name=department_name,
        is_active=True,
    ).first()

    if department is None:
        raise OverdueConfigurationError(
            (
                f"The escalation department '{department_name}' "
                "does not exist or is inactive."
            )
        )

    recipient_email = (
        department.email or ""
    ).strip()

    if not recipient_email:
        raise OverdueConfigurationError(
            (
                f"The escalation department '{department.name}' "
                "does not have an email address."
            )
        )

    return recipient_email


def get_overdue_notification_type(
    task: WorkflowTask,
) -> str:
    """
    Distinguish between an unopened and an incomplete task.
    """

    if task.opened_at is None:
        return "TASK_OVERDUE_UNOPENED"

    return "TASK_OVERDUE_INCOMPLETE"


def build_overdue_deduplication_key(
    task: WorkflowTask,
    reminder_date: date | None = None,
) -> str:
    """
    Build a unique key allowing one reminder per task per UTC day.
    """

    effective_date = reminder_date or utc_now().date()

    return (
        f"overdue-task:"
        f"{task.id}:"
        f"{effective_date.isoformat()}"
    )


def find_existing_overdue_notification(
    deduplication_key: str,
) -> EmailNotification | None:
    """
    Find today's existing reminder notification, if one exists.
    """

    return EmailNotification.query.filter_by(
        deduplication_key=deduplication_key
    ).first()