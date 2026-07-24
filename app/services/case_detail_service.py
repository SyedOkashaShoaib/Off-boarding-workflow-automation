from dataclasses import dataclass
from typing import List, Optional

from sqlalchemy.orm import (
    joinedload,
    selectinload,
)

from app.models import (
    AuditLog,
    ChecklistResponse,
    OffboardingCase,
    WorkflowPhase,
    WorkflowTask,
)
OPEN_TASK_STATUSES = (
    "PENDING",
    "IN_PROGRESS",
)
@dataclass(frozen=True)
class CaseDetailRecord:
    """
    Read-only data required by the NOC case-detail page.

    SQLAlchemy model instances remain attached to the active request
    session, while sorting and current-task resolution are completed
    before the template is rendered.
    """

    case: OffboardingCase
    tasks: List[WorkflowTask]
    current_task: Optional[WorkflowTask]
    audit_logs: List[AuditLog]
    final_task: Optional[WorkflowTask]
    final_approval_log: Optional[AuditLog]
    


def get_case_detail_record(
    case_id: int,
) -> Optional[CaseDetailRecord]:
    """
    Retrieve one offboarding case with its operational history.

    The related data is eagerly loaded to avoid repeated relationship
    queries while the Jinja template renders the case record.
    """

    case = (
        OffboardingCase.query
        .options(
            joinedload(
                OffboardingCase.current_phase
            ).joinedload(
                WorkflowPhase.department
            ),
            selectinload(
                OffboardingCase.tasks
            ).joinedload(
                WorkflowTask.phase
            ).joinedload(
                WorkflowPhase.department
            ),
            selectinload(
                OffboardingCase.tasks
            ).selectinload(
                WorkflowTask.responses
            ).joinedload(
                ChecklistResponse.checklist_item
            ),
            selectinload(
                OffboardingCase.tasks
            ).selectinload(
                WorkflowTask.notifications
            ),
            selectinload(
                OffboardingCase.audit_logs
            ),
        )
        .filter(
            OffboardingCase.id == case_id
        )
        .first()
    )

    if case is None:
        return None

    tasks = sorted(
        case.tasks,
        key=lambda task: (
            task.phase.phase_order,
            task.id,
        ),
    )

    # current_task = next(
    # (
    #     task
    #     for task in tasks
    #     if task.phase_id
    #     == case.current_phase_id
    # ),
    # None,
    # )
    current_task = None
    if case.status != 'CLOSED':
        current_task = next (
            (
                task
                for task in tasks
                if (
                    task.phase_id == case.current_phase_id and task.status in OPEN_TASK_STATUSES
                )
            ), None,
        )

    audit_logs = sorted(
        case.audit_logs,
        key=lambda audit_log: (
        audit_log.created_at,
        audit_log.id,
    ), reverse=True,
    )

    final_task = next(
        (
            task
            for task in tasks
            if task.phase.is_final_approval
        ),
        None,
)

    final_approval_log = next(
        (
            audit_log
            for audit_log in audit_logs
            if audit_log.action == "FINAL_APPROVAL_GRANTED"
        ),
    None,
)

    return CaseDetailRecord(
        case=case,
        tasks=tasks,
        current_task=current_task,
        final_task=final_task,
        final_approval_log=final_approval_log,
        audit_logs=audit_logs,
    )