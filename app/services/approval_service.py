from app.extension import db
from app.models import (
    AuditLog,
    WorkflowPhase,
    WorkflowTask,
    utc_now,
)


MAX_APPROVAL_REMARKS_LENGTH = 2000


class FinalApprovalError(Exception):
    """Raised when a case cannot be approved and closed safely."""


def get_prior_phase_completion_issues(
    final_task: WorkflowTask,
) -> list[str]:
    """
    Check that every active phase before the final approval phase
    has a completed workflow task.

    Returns:
        A list of human-readable blocking issues.
    """

    prior_phases = (
        WorkflowPhase.query
        .filter(
            WorkflowPhase.is_active.is_(True),
            WorkflowPhase.phase_order
            < final_task.phase.phase_order,
        )
        .order_by(
            WorkflowPhase.phase_order.asc(),
            WorkflowPhase.id.asc(),
        )
        .all()
    )

    tasks_by_phase_id = {
        task.phase_id: task
        for task in final_task.case.tasks
    }

    issues: list[str] = []

    for phase in prior_phases:
        prior_task = tasks_by_phase_id.get(phase.id)

        if prior_task is None:
            issues.append(
                f"No workflow task exists for '{phase.name}'."
            )
            continue

        if (
            prior_task.status != "SUBMITTED"
            or prior_task.submitted_at is None
        ):
            issues.append(
                (
                    f"The task for '{phase.name}' has not been "
                    "submitted successfully."
                )
            )

    return issues


def approve_and_close_case(
    *,
    final_task: WorkflowTask,
    approved_by: str,
    remarks: str = "",
) -> None:
    """
    Approve the final workflow task and close its offboarding case.

    This function modifies the SQLAlchemy session but does not
    commit. The route controls the transaction.
    """

    if not final_task.phase.is_final_approval:
        raise FinalApprovalError(
            "This workflow task is not a final approval task."
        )

    if final_task.case.current_phase_id != final_task.phase_id:
        raise FinalApprovalError(
            (
                "This task is not the current active phase for "
                "the offboarding case."
            )
        )

    if (
        final_task.status == "APPROVED"
        or final_task.case.status == "CLOSED"
        or final_task.case.closed_at is not None
    ):
        raise FinalApprovalError(
            "This offboarding case has already been closed."
        )

    completion_issues = get_prior_phase_completion_issues(
        final_task
    )

    if completion_issues:
        raise FinalApprovalError(
            (
                "The case cannot be closed because previous "
                "workflow phases are incomplete: "
                + " ".join(completion_issues)
            )
        )

    cleaned_approved_by = (approved_by or "").strip()

    if not cleaned_approved_by:
        raise FinalApprovalError(
            "The approving user could not be identified."
        )

    cleaned_remarks = (remarks or "").strip()

    if len(cleaned_remarks) > MAX_APPROVAL_REMARKS_LENGTH:
        raise FinalApprovalError(
            (
                "Final approval remarks cannot exceed "
                f"{MAX_APPROVAL_REMARKS_LENGTH} characters."
            )
        )

    approved_at = utc_now()

    final_task.status = "APPROVED"
    final_task.submitted_at = approved_at

    final_task.case.status = "CLOSED"
    final_task.case.closed_at = approved_at

    db.session.add(
        AuditLog(
            case=final_task.case,
            action="FINAL_APPROVAL_GRANTED",
            performed_by=cleaned_approved_by,
            details=(
                f"Final approval was granted for workflow task "
                f"{final_task.id}. "
                f"Remarks: {cleaned_remarks or 'None provided.'} "
                "The approving identity has not yet been verified "
                "through authentication."
            ),
        )
    )

    db.session.add(
        AuditLog(
            case=final_task.case,
            action="CASE_CLOSED",
            performed_by=cleaned_approved_by,
            details=(
                f"Offboarding case "
                f"{final_task.case.case_number} was closed after "
                "successful completion of all workflow phases."
            ),
        )
    )