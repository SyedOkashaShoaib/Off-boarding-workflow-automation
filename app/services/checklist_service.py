from collections.abc import Mapping
from typing import Any

from app.extension import db
from app.models import (
    AuditLog,
    ChecklistResponse,
    WorkflowTask,
    utc_now,
)


ALLOWED_RESPONSE_STATUSES = {
    "YES",
    "NOT_APPLICABLE",
}

MAX_REASON_LENGTH = 2000


class ChecklistSubmissionError(Exception):
    """Raised when a checklist cannot be submitted safely."""


def get_active_checklist_items(task: WorkflowTask):
    """
    Return active checklist items for the task's workflow phase.
    """

    return [
        checklist_item
        for checklist_item in task.phase.checklist_items
        if checklist_item.is_active
    ]


def validate_checklist_submission(
    task: WorkflowTask,
    form_data: Mapping[str, Any],
) -> tuple[dict[int, dict[str, str]], dict[int, str]]:
    """
    Validate dynamically generated checklist fields.

    Returns:
        submitted_values:
            Cleaned values indexed by checklist-item ID.

        validation_errors:
            Error messages indexed by checklist-item ID.
    """

    submitted_values: dict[int, dict[str, str]] = {}
    validation_errors: dict[int, str] = {}

    checklist_items = get_active_checklist_items(task)

    for checklist_item in checklist_items:
        response_field = f"response_{checklist_item.id}"
        reason_field = f"reason_{checklist_item.id}"

        response_status = str(
            form_data.get(response_field, "")
        ).strip().upper()

        reason = str(
            form_data.get(reason_field, "")
        ).strip()

        submitted_values[checklist_item.id] = {
            "response_status": response_status,
            "reason": reason,
        }

        if not response_status:
            validation_errors[checklist_item.id] = (
                "Select YES or NOT APPLICABLE."
            )
            continue

        if response_status not in ALLOWED_RESPONSE_STATUSES:
            validation_errors[checklist_item.id] = (
                "The selected response is not valid."
            )
            continue

        if (
            response_status == "NOT_APPLICABLE"
            and not reason
        ):
            validation_errors[checklist_item.id] = (
                "A reason is required when selecting "
                "NOT APPLICABLE."
            )
            continue

        if len(reason) > MAX_REASON_LENGTH:
            validation_errors[checklist_item.id] = (
                f"The reason cannot exceed "
                f"{MAX_REASON_LENGTH} characters."
            )
            continue

        if response_status == "YES":
            submitted_values[checklist_item.id]["reason"] = ""

    return submitted_values, validation_errors


def persist_checklist_submission(
    task: WorkflowTask,
    submitted_values: dict[int, dict[str, str]],
    responded_by: str,
) -> int:
    """
    Persist all checklist responses and mark the task submitted.

    This function modifies the current SQLAlchemy session but does
    not commit. The route controls the transaction.

    Returns:
        Number of responses created.
    """

    if task.status == "SUBMITTED" or task.submitted_at is not None:
        raise ChecklistSubmissionError(
            "This workflow task has already been submitted."
        )

    checklist_items = get_active_checklist_items(task)

    if not checklist_items:
        raise ChecklistSubmissionError(
            "No active checklist items are configured for this phase."
        )

    if task.responses:
        raise ChecklistSubmissionError(
            "Checklist responses already exist for this task."
        )

    created_response_count = 0

    for checklist_item in checklist_items:
        submitted_value = submitted_values.get(
            checklist_item.id
        )

        if submitted_value is None:
            raise ChecklistSubmissionError(
                "The checklist submission is incomplete."
            )

        response = ChecklistResponse(
            case_id=task.case_id,
            workflow_task=task,
            checklist_item=checklist_item,
            response_status=submitted_value[
                "response_status"
            ],
            not_applicable_reason=(
                submitted_value["reason"] or None
            ),
            responded_by=responded_by,
        )

        db.session.add(response)
        created_response_count += 1

    task.status = "SUBMITTED"
    task.submitted_at = utc_now()

    db.session.add(
        AuditLog(
            case=task.case,
            action="TASK_SUBMITTED",
            performed_by=responded_by,
            details=(
                f"Workflow task {task.id} for phase "
                f"'{task.phase.name}' was submitted with "
                f"{created_response_count} checklist responses. "
                "The responder identity has not yet been verified "
                "through authentication."
            ),
        )
    )

    return created_response_count