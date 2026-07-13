from flask import (
    Blueprint,
    current_app,
    flash,
    render_template,
)
from sqlalchemy.exc import SQLAlchemyError

from app.extension import db
from app.models import (
    AuditLog,
    WorkflowTask,
    utc_now,
)

workflow_bp = Blueprint('workflow', __name__, url_prefix='/workflow')

@workflow_bp.route('/tasks/<int:task_id>', methods=['GET'])
def view_task(task_id):
    task = WorkflowTask.query.get_or_404(task_id)

    if task.opened_at is None:
        try:
            task.opened_at = utc_now()
            if task.status == 'PENDING':
                task.status = 'IN_PROGRESS'
            db.session.add(AuditLog(case=task.case,
                                    action='TASK_OPENED',
                                    performed_by='System',
                                    details=(
                                        f"Workflow task {task.id} was opened through"
                                        "its assigned link."
                                    ),))
            db.session.commit()

        except SQLAlchemyError:
            db.session.rollback()
            current_app.logger.exception(
                "Failed to reccord the opening of workflow task %s.", task_id
            )
            flash(
                ("The task was loaded, but the system could not record the opening of its opened timestamp"), "WARNING"
            )

        checklist_sections = {}
        for checklist_item in task.phase.checklist_items:
            if not checklist_item.is_active:
                continue
            section_name = checklist_item.section or 'Checklist'

            checklist_sections.setdefault(
            section_name,
            [],
        ).append(checklist_item)

        return render_template(
            'workflow/task_detail.html', task=task, checklist_sections=checklist_sections
        )