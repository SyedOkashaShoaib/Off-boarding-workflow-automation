from datetime import timedelta

from app.extension import db
from app.models import (
    AuditLog,
    OffboardingCase,
    WorkflowPhase,
    WorkflowTask,
    utc_now,
)


class WorkflowConfigurationError(Exception):
    """Raised when workflow master data is incomplete."""


class WorkflowTransitionError(Exception):
    """Raised when a case cannot advance to the next phase."""


def validate_phase_assignment(
    phase: WorkflowPhase,
) -> str:
    """
    Validate that a workflow phase has an active department
    and a usable notification email.

    Returns:
        The cleaned department email address.
    """

    if phase.department is None:
        raise WorkflowConfigurationError(
            f"Workflow phase '{phase.name}' has no department."
        )

    if not phase.department.is_active:
        raise WorkflowConfigurationError(
            f"Department '{phase.department.name}' is inactive."
        )

    department_email = (
        phase.department.email or ""
    ).strip()

    if not department_email:
        raise WorkflowConfigurationError(
            f"Department '{phase.department.name}' "
            "has no notification email."
        )

    return department_email


def get_first_active_phase() -> WorkflowPhase:
    """Return the first active workflow phase."""

    first_phase = (
        WorkflowPhase.query
        .filter_by(is_active=True)
        .order_by(
            WorkflowPhase.phase_order.asc(),
            WorkflowPhase.id.asc(),
        )
        .first()
    )

    if first_phase is None:
        raise WorkflowConfigurationError(
            "No active workflow phases are configured."
        )

    return first_phase


def get_next_active_phase(
    current_phase: WorkflowPhase,
) -> WorkflowPhase:
    """
    Return the next active workflow phase after the supplied phase.
    """

    next_phase = (
        WorkflowPhase.query
        .filter(
            WorkflowPhase.is_active.is_(True),
            WorkflowPhase.phase_order
            > current_phase.phase_order,
        )
        .order_by(
            WorkflowPhase.phase_order.asc(),
            WorkflowPhase.id.asc(),
        )
        .first()
    )

    if next_phase is None:
        raise WorkflowConfigurationError(
            f"No active workflow phase exists after "
            f"'{current_phase.name}'."
        )

    return next_phase


def create_initial_workflow_task(
    offboarding_case: OffboardingCase,
) -> WorkflowTask:
    """
    Create the initial workflow task for a new offboarding case.

    This function does not commit the database transaction.
    """

    first_phase = get_first_active_phase()

    department_email = validate_phase_assignment(
        first_phase
    )

    assigned_at = utc_now()

    task = WorkflowTask(
        case=offboarding_case,
        phase=first_phase,
        assigned_to_email=department_email,
        status="PENDING",
        assigned_at=assigned_at,
        due_at=assigned_at + timedelta(days=7),
    )

    offboarding_case.current_phase = first_phase
    offboarding_case.status = "IN_PROGRESS"

    db.session.add(task)

    db.session.add(
        AuditLog(
            case=offboarding_case,
            action="INITIAL_TASK_CREATED",
            performed_by="System",
            details=(
                f"Initial workflow task created for phase "
                f"'{first_phase.name}' and assigned to "
                f"'{department_email}'."
            ),
        )
    )

    return task


def create_next_workflow_task(
    completed_task: WorkflowTask,
) -> WorkflowTask:
    """
    Create the next departmental task after successful submission
    of the current task.

    This function does not commit the database transaction.
    """

    if (
        completed_task.status != "SUBMITTED"
        or completed_task.submitted_at is None
    ):
        raise WorkflowTransitionError(
            "The current workflow task must be submitted "
            "before the workflow can advance."
        )

    if completed_task.phase.is_final_approval:
        raise WorkflowTransitionError(
            "A final approval task cannot advance to another phase."
        )

    next_phase = get_next_active_phase(
        completed_task.phase
    )

    department_email = validate_phase_assignment(
        next_phase
    )

    existing_task = (
        WorkflowTask.query
        .filter_by(
            case_id=completed_task.case_id,
            phase_id=next_phase.id,
        )
        .first()
    )

    if existing_task is not None:
        raise WorkflowTransitionError(
            f"A workflow task for phase '{next_phase.name}' "
            f"already exists for case "
            f"{completed_task.case.case_number}."
        )

    assigned_at = utc_now()

    next_task = WorkflowTask(
        case=completed_task.case,
        phase=next_phase,
        assigned_to_email=department_email,
        status="PENDING",
        assigned_at=assigned_at,
        due_at=assigned_at + timedelta(days=7),
    )

    completed_task.case.current_phase = next_phase
    completed_task.case.status = "IN_PROGRESS"

    db.session.add(next_task)

    db.session.add(
        AuditLog(
            case=completed_task.case,
            action="NEXT_TASK_CREATED",
            performed_by="System",
            details=(
                f"Workflow advanced from phase "
                f"'{completed_task.phase.name}' to "
                f"'{next_phase.name}'. The new task was assigned "
                f"to '{department_email}'."
            ),
        )
    )

    return next_task