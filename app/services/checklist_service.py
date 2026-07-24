from collections import Counter
from collections.abc import Mapping
from typing import Any, Dict, List, Tuple

from app.extension import db

from app.models import (
    AuditLog,
    ChecklistResponse,
    DepartmentEmployee,
    WorkflowTask,
    utc_now,
)


ALLOWED_RESPONSE_STATUSES = {
    "YES",
    "NO",
    "NOT_APPLICABLE",
}


REASON_REQUIRED_RESPONSE_STATUSES = {
    "NO",
    "NOT_APPLICABLE",
}


MAX_REASON_LENGTH = 2000


class ChecklistSubmissionError(Exception):
    """
    Raised when a checklist cannot be submitted safely.
    """


def get_active_checklist_items(
    task: WorkflowTask,
):
    """
    Return active checklist items for the task's workflow phase.
    """

    return [
        checklist_item
        for checklist_item in task.phase.checklist_items
        if checklist_item.is_active
    ]


def get_active_department_employees(
    task: WorkflowTask,
) -> List[DepartmentEmployee]:
    """
    Return active employees belonging to the department responsible
    for the supplied workflow task.

    The permitted department is derived from server-side workflow
    state, not from a browser-submitted department value.
    """

    if task.phase is None:
        return []

    if task.phase.department_id is None:
        return []

    return (
        DepartmentEmployee.query
        .filter_by(
            department_id=task.phase.department_id,
            is_active=True,
        )
        .order_by(
            DepartmentEmployee.full_name.asc(),
            DepartmentEmployee.id.asc(),
        )
        .all()
    )


def validate_checklist_submission(
    task: WorkflowTask,
    form_data: Mapping[str, Any],
    department_employees: List[DepartmentEmployee],
) -> Tuple[
    Dict[int, Dict[str, Any]],
    Dict[int, str],
]:
    """
    Validate dynamically generated checklist fields.

    Expected fields for each checklist item:

    - response_<item_id>
    - reason_<item_id>
    - responsible_employee_<item_id>

    Returns:

    submitted_values:
        Cleaned values indexed by checklist-item ID.

    validation_errors:
        One combined error message indexed by checklist-item ID.
    """

    submitted_values: Dict[
        int,
        Dict[str, Any],
    ] = {}

    validation_errors: Dict[int, str] = {}

    checklist_items = get_active_checklist_items(
        task
    )

    eligible_employees_by_id = {
        employee.id: employee
        for employee in department_employees
        if (
            employee.is_active
            and employee.department_id
            == task.phase.department_id
        )
    }

    for checklist_item in checklist_items:
        response_field = (
            f"response_{checklist_item.id}"
        )

        reason_field = (
            f"reason_{checklist_item.id}"
        )

        employee_field = (
            "responsible_employee_"
            f"{checklist_item.id}"
        )

        response_status = str(
            form_data.get(
                response_field,
                "",
            )
        ).strip().upper()

        reason = str(
            form_data.get(
                reason_field,
                "",
            )
        ).strip()

        raw_employee_id = str(
            form_data.get(
                employee_field,
                "",
            )
        ).strip()

        responsible_employee_id = None

        item_errors: List[str] = []

        if not response_status:
            item_errors.append(
                (
                    "Select YES, NO, or "
                    "NOT APPLICABLE."
                )
            )

        elif (
            response_status
            not in ALLOWED_RESPONSE_STATUSES
        ):
            item_errors.append(
                "The selected response is not valid."
            )

        if (
            response_status
            in REASON_REQUIRED_RESPONSE_STATUSES
            and not reason
        ):
            item_errors.append(
                (
                    "A reason is required when selecting "
                    "NO or NOT APPLICABLE."
                )
            )

        if len(reason) > MAX_REASON_LENGTH:
            item_errors.append(
                (
                    "The reason cannot exceed "
                    f"{MAX_REASON_LENGTH} characters."
                )
            )

        if response_status == "YES":
            reason = ""

        if not raw_employee_id:
            item_errors.append(
                "Select the responsible employee."
            )

        else:
            try:
                responsible_employee_id = int(
                    raw_employee_id
                )

            except (TypeError, ValueError):
                item_errors.append(
                    (
                        "The selected responsible employee "
                        "is not valid."
                    )
                )

            else:
                if (
                    responsible_employee_id
                    not in eligible_employees_by_id
                ):
                    item_errors.append(
                        (
                            "Select an active employee from "
                            "the assigned department."
                        )
                    )

        submitted_values[
            checklist_item.id
        ] = {
            "response_status": response_status,
            "reason": reason,
            "responsible_employee_id": (
                responsible_employee_id
                if responsible_employee_id is not None
                else raw_employee_id
            ),
        }

        if item_errors:
            validation_errors[
                checklist_item.id
            ] = " ".join(item_errors)

    return (
        submitted_values,
        validation_errors,
    )


def persist_checklist_submission(
    task: WorkflowTask,
    submitted_values: Dict[
        int,
        Dict[str, Any],
    ],
    responded_by: str,
) -> int:
    """
    Persist all checklist responses and mark the task submitted.

    This function modifies the current SQLAlchemy session but does
    not commit. The workflow route owns the transaction.

    The validation is repeated defensively because this function
    must remain safe even if called from somewhere other than the
    normal checklist route.
    """

    if (
        task.status == "SUBMITTED"
        or task.submitted_at is not None
    ):
        raise ChecklistSubmissionError(
            (
                "This workflow task has already "
                "been submitted."
            )
        )

    checklist_items = get_active_checklist_items(
        task
    )

    if not checklist_items:
        raise ChecklistSubmissionError(
            (
                "No active checklist items are "
                "configured for this phase."
            )
        )

    if task.responses:
        raise ChecklistSubmissionError(
            (
                "Checklist responses already exist "
                "for this task."
            )
        )

    expected_item_ids = {
        checklist_item.id
        for checklist_item in checklist_items
    }

    submitted_item_ids = set(
        submitted_values.keys()
    )

    if submitted_item_ids != expected_item_ids:
        raise ChecklistSubmissionError(
            "The checklist submission is incomplete."
        )

    responsible_employee_ids = set()

    for checklist_item in checklist_items:
        submitted_value = submitted_values.get(
            checklist_item.id
        )

        if submitted_value is None:
            raise ChecklistSubmissionError(
                "The checklist submission is incomplete."
            )

        raw_employee_id = submitted_value.get(
            "responsible_employee_id"
        )

        try:
            employee_id = int(
                raw_employee_id
            )

        except (TypeError, ValueError):
            raise ChecklistSubmissionError(
                (
                    "One or more responsible employee "
                    "selections are invalid."
                )
            )

        responsible_employee_ids.add(
            employee_id
        )

    eligible_employees = (
        DepartmentEmployee.query
        .filter(
            DepartmentEmployee.id.in_(
                responsible_employee_ids
            ),
            DepartmentEmployee.department_id
            == task.phase.department_id,
            DepartmentEmployee.is_active.is_(
                True
            ),
        )
        .all()
    )

    eligible_employees_by_id = {
        employee.id: employee
        for employee in eligible_employees
    }

    if (
        len(eligible_employees_by_id)
        != len(responsible_employee_ids)
    ):
        raise ChecklistSubmissionError(
            (
                "One or more selected employees are "
                "inactive or do not belong to the "
                "assigned department."
            )
        )

    normalized_responded_by = str(
        responded_by or ""
    ).strip().lower()

    if not normalized_responded_by:
        raise ChecklistSubmissionError(
            (
                "The department submission email "
                "could not be determined."
            )
        )

    response_counts = Counter()

    created_response_count = 0

    for checklist_item in checklist_items:
        submitted_value = submitted_values[
            checklist_item.id
        ]

        response_status = str(
            submitted_value.get(
                "response_status",
                "",
            )
        ).strip().upper()

        reason = str(
            submitted_value.get(
                "reason",
                "",
            )
        ).strip()

        if (
            response_status
            not in ALLOWED_RESPONSE_STATUSES
        ):
            raise ChecklistSubmissionError(
                (
                    "One or more checklist responses "
                    "are invalid."
                )
            )

        if (
            response_status
            in REASON_REQUIRED_RESPONSE_STATUSES
            and not reason
        ):
            raise ChecklistSubmissionError(
                (
                    "A reason is required for every "
                    "NO or NOT APPLICABLE response."
                )
            )

        if len(reason) > MAX_REASON_LENGTH:
            raise ChecklistSubmissionError(
                (
                    "One or more checklist reasons "
                    "exceed the permitted length."
                )
            )

        if response_status == "YES":
            reason = ""

        employee_id = int(
            submitted_value[
                "responsible_employee_id"
            ]
        )

        responsible_employee = (
            eligible_employees_by_id.get(
                employee_id
            )
        )

        if responsible_employee is None:
            raise ChecklistSubmissionError(
                (
                    "One or more responsible employee "
                    "selections are no longer valid."
                )
            )

        response = ChecklistResponse(
            case_id=task.case_id,
            workflow_task=task,
            checklist_item=checklist_item,
            responsible_employee=(
                responsible_employee
            ),
            response_status=response_status,
            response_reason=(
                reason or None
            ),
            responded_by=(
                normalized_responded_by
            ),
        )

        db.session.add(
            response
        )

        response_counts[
            response_status
        ] += 1

        created_response_count += 1

    task.status = "SUBMITTED"
    task.submitted_at = utc_now()

    db.session.add(
        AuditLog(
            case=task.case,
            action="TASK_SUBMITTED",
            performed_by=(
                normalized_responded_by
            ),
            details=(
                f"Workflow task {task.id} for phase "
                f"'{task.phase.name}' was submitted with "
                f"{created_response_count} checklist "
                "responses: "
                f"{response_counts['YES']} Yes, "
                f"{response_counts['NO']} No, and "
                f"{response_counts['NOT_APPLICABLE']} "
                "Not applicable."
            ),
        )
    )

    return created_response_count