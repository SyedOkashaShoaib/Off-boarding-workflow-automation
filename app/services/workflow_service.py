from app.extension import db
from datetime import timedelta
from app.models import WorkflowPhase, WorkflowTask,AuditLog, utc_now


class WorkflowConfigurationError(Exception):
     pass

def get_first_active_phase(self):
    first_phase = WorkflowPhase.query.filter_by(is_active=True).order_by(WorkflowPhase.phase_order.asc()).first()
    if first_phase is None:
        raise WorkflowConfigurationError(
            'No active workflow phases found in the database :('
        )
    return first_phase
    
def create_initial_workflow_task(self, offboarding_case):
    first_phase = get_first_active_phase()

    if first_phase.department is None:
        raise WorkflowConfigurationError(
            f"Phase {first_phase.name} has no assigned department"
        )
    # if first_phase.department.email is None:
    #     raise WorkflowConfigurationError(
    #         f"Phase {first_phase.name} has no assigned department's email"
    #     )
    assigned_at = utc_now()
    due_at = utc_now() + 7 #instead of hardcoding 7, why not make it a variabe in cnofig file?
    offboarding_case.current_phase = first_phase
    offboarding_case.status = 'IN_PROGRESS'
    task = WorkflowTask(
        case = offboarding_case,
        phase = first_phase,
        assigned_to_email = first_phase.department.email,
        status = 'PENDING',
        assigned_at=assigned_at,
        due_at=due_at
    )

    db.session.add(task)

    audit_log = AuditLog(
        case=offboarding_case,
        action='INITIAL_TASK_CREATED',
        performed_by = 'System',
        details = f"Initial workflow task created for {first_phase.name} assiigned to {first_phase.department.name}",

    )
    return task

