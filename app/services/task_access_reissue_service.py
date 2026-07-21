from dataclasses import dataclass

from app.models import (
    EmailNotification,
    OffboardingCase,
    WorkflowTask,
)

from app.services.email_service import (
    EmailResult,
)

from app.services.notification_service import (
    create_task_access_reissue_notification,
    deliver_task_assignment_notification,
    task_requires_portal_login,
)


OPEN_TASK_STATUSES = {
    "PENDING",
    "IN_PROGRESS",
}

MINIMUM_REASON_LENGTH = 10
MAXIMUM_REASON_LENGTH = 500


class TaskAccessReissueError(Exception):
    """
    Raised when a replacement secure link cannot be issued.
    """


@dataclass(frozen=True)
class TaskAccessReissueResult:
    """
    Result produced by one secure-link reissue attempt.
    """

    task: WorkflowTask
    notification: EmailNotification
    delivery_result: EmailResult


def normalize_reissue_reason(
    reason: str,
) -> str:
    """
    Validate and normalize the operational reason supplied by NOC.
    """

    normalized_reason = str(
        reason or ""
    ).strip()

    if len(normalized_reason) < MINIMUM_REASON_LENGTH:
        raise TaskAccessReissueError(
            (
                "A reissue reason of at least "
                f"{MINIMUM_REASON_LENGTH} characters is required."
            )
        )

    if len(normalized_reason) > MAXIMUM_REASON_LENGTH:
        raise TaskAccessReissueError(
            (
                "The reissue reason cannot exceed "
                f"{MAXIMUM_REASON_LENGTH} characters."
            )
        )

    return normalized_reason


def get_reissuable_current_task(
    case: OffboardingCase,
) -> WorkflowTask:
    """
    Resolve and validate the case's current token-based task.

    The browser is not permitted to select an arbitrary task or
    department. The current task is derived from database state.
    """

    if case.status == "CLOSED":
        raise TaskAccessReissueError(
            "Closed cases cannot receive replacement links."
        )

    if case.current_phase_id is None:
        raise TaskAccessReissueError(
            "The case does not have a current workflow phase."
        )

    task = (
        WorkflowTask.query
        .filter_by(
            case_id=case.id,
            phase_id=case.current_phase_id,
        )
        .first()
    )

    if task is None:
        raise TaskAccessReissueError(
            (
                "The current workflow task could not be "
                "resolved for this case."
            )
        )

    if task.status not in OPEN_TASK_STATUSES:
        raise TaskAccessReissueError(
            (
                "Only pending or in-progress tasks can "
                "receive replacement links."
            )
        )

    if task.phase is None:
        raise TaskAccessReissueError(
            "The workflow task has no configured phase."
        )

    if task.phase.department is None:
        raise TaskAccessReissueError(
            "The workflow phase has no assigned department."
        )

    if task_requires_portal_login(task):
        raise TaskAccessReissueError(
            (
                "NOC tasks use portal authentication and "
                "cannot receive secure task links."
            )
        )

    assigned_email = str(
        task.assigned_to_email or ""
    ).strip()

    if not assigned_email:
        raise TaskAccessReissueError(
            (
                "The current task does not have a valid "
                "recipient email address."
            )
        )

    return task


def reissue_current_task_access(
    *,
    case: OffboardingCase,
    requested_by: str,
    reason: str,
) -> TaskAccessReissueResult:
    """
    Issue and deliver a replacement secure link for the current
    eligible workflow task.

    The caller owns the surrounding database transaction and must
    commit the notification, grant, revocations, and audit events.
    """

    normalized_actor = str(
        requested_by or ""
    ).strip().lower()

    if not normalized_actor:
        raise TaskAccessReissueError(
            "The requesting portal user could not be identified."
        )

    normalized_reason = normalize_reissue_reason(
        reason
    )

    task = get_reissuable_current_task(
        case
    )

    notification = (
        create_task_access_reissue_notification(
            task=task,
            requested_by=normalized_actor,
            reason=normalized_reason,
        )
    )

    delivery_result = (
        deliver_task_assignment_notification(
            notification
        )
    )

    return TaskAccessReissueResult(
        task=task,
        notification=notification,
        delivery_result=delivery_result,
    )