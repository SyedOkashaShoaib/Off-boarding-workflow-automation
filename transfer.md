from datetime import date
from typing import Optional

from sqlalchemy.orm import joinedload

from app.models import (
    EmailNotification,
    OffboardingCase,
    WorkflowPhase,
    WorkflowTask,
    utc_now,
)


OPEN_TASK_STATUSES = (
    "PENDING",
    "IN_PROGRESS",
)


def find_current_active_tasks(
    task_id: Optional[int] = None,
) -> list[WorkflowTask]:
    """
    Return the current open task for every non-closed case.

    A task is eligible when:
    - its status is PENDING or IN_PROGRESS;
    - its case is not CLOSED; and
    - its phase is the case's current workflow phase.

    Supplying task_id limits processing to one task without
    bypassing any of the normal eligibility conditions.
    """

    query = (
        WorkflowTask.query
        .join(
            OffboardingCase,
            WorkflowTask.case_id
            == OffboardingCase.id,
        )
        .options(
            joinedload(
                WorkflowTask.case
            ),
            joinedload(
                WorkflowTask.phase
            ).joinedload(
                WorkflowPhase.department
            ),
        )
        .filter(
            WorkflowTask.status.in_(
                OPEN_TASK_STATUSES
            ),
            OffboardingCase.status != "CLOSED",
            OffboardingCase.current_phase_id.isnot(
                None
            ),
            WorkflowTask.phase_id
            == OffboardingCase.current_phase_id,
        )
        .order_by(
            WorkflowTask.assigned_at.asc(),
            WorkflowTask.id.asc(),
        )
    )

    if task_id is not None:
        query = query.filter(
            WorkflowTask.id == task_id
        )

    return query.all()


def build_daily_task_reminder_key(
    task: WorkflowTask,
    reminder_date: Optional[date] = None,
) -> str:
    """
    Build the unique key used to permit one successful reminder
    per workflow task per UTC calendar day.
    """

    effective_date = (
        reminder_date
        or utc_now().date()
    )

    return (
        "daily-task-reminder:"
        f"{task.id}:"
        f"{effective_date.isoformat()}"
    )


def find_existing_daily_task_reminder(
    deduplication_key: str,
) -> Optional[EmailNotification]:
    """
    Return today's reminder notification for the supplied task,
    when one has already been created.
    """

    return (
        EmailNotification.query
        .filter_by(
            deduplication_key=deduplication_key
        )
        .first()
    )