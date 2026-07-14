from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from sqlalchemy.exc import SQLAlchemyError

from app.extension import db
from app.forms.workflow_forms import WorkflowChecklistForm
from app.models import (
    AuditLog,
    WorkflowTask,
    utc_now,
)
from app.services.checklist_service import (
    ChecklistSubmissionError,
    persist_checklist_submission,
    validate_checklist_submission,
)
from app.services.notification_service import (
    create_task_assignment_notification,
    deliver_task_assignment_notification,
)
from app.services.workflow_service import (
    WorkflowConfigurationError,
    WorkflowTransitionError,
    create_next_workflow_task,
)


workflow_bp = Blueprint(
    "workflow",
    __name__,
    url_prefix="/workflow",
)


def build_checklist_sections(
    task: WorkflowTask,
) -> dict[str, list]:
    """Group active checklist items by database section."""

    checklist_sections: dict[str, list] = {}

    for checklist_item in task.phase.checklist_items:
        if not checklist_item.is_active:
            continue

        section_name = (
            checklist_item.section or "Checklist"
        )

        checklist_sections.setdefault(
            section_name,
            [],
        ).append(checklist_item)

    return checklist_sections


def build_saved_response_values(
    task: WorkflowTask,
) -> dict[int, dict[str, str]]:
    """
    Convert saved ChecklistResponse records into values that can
    be displayed by the task template.
    """

    return {
        response.checklist_item_id: {
            "response_status": response.response_status,
            "reason": (
                response.not_applicable_reason or ""
            ),
        }
        for response in task.responses
    }


def record_task_opening(
    task: WorkflowTask,
) -> None:
    """Record only the first time a workflow task is opened."""

    if task.opened_at is not None:
        return

    try:
        task.opened_at = utc_now()

        if task.status == "PENDING":
            task.status = "IN_PROGRESS"

        db.session.add(
            AuditLog(
                case=task.case,
                action="TASK_OPENED",
                performed_by="System",
                details=(
                    f"Workflow task {task.id} was opened through "
                    "its assigned task link. The user's identity "
                    "has not yet been authenticated."
                ),
            )
        )

        db.session.commit()

    except SQLAlchemyError:
        db.session.rollback()

        current_app.logger.exception(
            "Failed to record workflow task %s as opened.",
            task.id,
        )

        flash(
            (
                "The task was loaded, but the system could not "
                "record its opened timestamp."
            ),
            "warning",
        )


@workflow_bp.route(
    "/tasks/<int:task_id>",
    methods=["GET", "POST"],
)
def view_task(task_id):
    """
    Display and submit a departmental workflow checklist.

    On successful submission:
    - save the current checklist;
    - mark the current task submitted;
    - create the next workflow task;
    - queue the next assignment notification;
    - attempt notification delivery.
    """

    task = WorkflowTask.query.get_or_404(task_id)

    record_task_opening(task)

    form = WorkflowChecklistForm()

    checklist_sections = build_checklist_sections(task)

    submitted_values = build_saved_response_values(
        task
    )

    validation_errors: dict[int, str] = {}

    if request.method == "POST":

        if task.status == "SUBMITTED":
            flash(
                "This workflow task has already been submitted.",
                "warning",
            )

            return redirect(
                url_for(
                    "workflow.view_task",
                    task_id=task.id,
                )
            )

        if task.phase.is_final_approval:
            flash(
                (
                    "Final approval tasks cannot be submitted "
                    "through the departmental checklist form."
                ),
                "error",
            )

            return redirect(
                url_for(
                    "workflow.view_task",
                    task_id=task.id,
                )
            )

        if not checklist_sections:
            flash(
                (
                    "This task cannot be submitted because no "
                    "active checklist items are configured."
                ),
                "error",
            )

            return render_template(
                "workflow/task_detail.html",
                task=task,
                form=form,
                checklist_sections=checklist_sections,
                submitted_values=submitted_values,
                validation_errors=validation_errors,
            )

        if not form.validate_on_submit():
            flash(
                (
                    "The form could not be validated. Refresh the "
                    "page and submit the checklist again."
                ),
                "error",
            )

            return render_template(
                "workflow/task_detail.html",
                task=task,
                form=form,
                checklist_sections=checklist_sections,
                submitted_values=submitted_values,
                validation_errors=validation_errors,
            )

        submitted_values, validation_errors = (
            validate_checklist_submission(
                task=task,
                form_data=request.form,
            )
        )

        if validation_errors:
            flash(
                (
                    "The checklist contains validation errors. "
                    "Correct the listed items and submit again."
                ),
                "error",
            )

            return render_template(
                "workflow/task_detail.html",
                task=task,
                form=form,
                checklist_sections=checklist_sections,
                submitted_values=submitted_values,
                validation_errors=validation_errors,
            )

        # -----------------------------------------------------
        # Transaction 1:
        # Save the checklist and create the next task.
        # -----------------------------------------------------
        try:
            response_count = persist_checklist_submission(
                task=task,
                submitted_values=submitted_values,
                responded_by=task.assigned_to_email,
            )

            next_task = create_next_workflow_task(
                completed_task=task,
            )

            notification = (
                create_task_assignment_notification(
                    next_task
                )
            )

            db.session.commit()

        except (
            ChecklistSubmissionError,
            WorkflowConfigurationError,
            WorkflowTransitionError,
        ) as exc:
            db.session.rollback()

            flash(
                str(exc),
                "error",
            )

            return render_template(
                "workflow/task_detail.html",
                task=task,
                form=form,
                checklist_sections=checklist_sections,
                submitted_values=submitted_values,
                validation_errors=validation_errors,
            )

        except SQLAlchemyError:
            db.session.rollback()

            current_app.logger.exception(
                (
                    "Database error while submitting task %s "
                    "and advancing the workflow."
                ),
                task.id,
            )

            flash(
                (
                    "A database error occurred. The checklist was "
                    "not submitted and the workflow was not advanced."
                ),
                "error",
            )

            return render_template(
                "workflow/task_detail.html",
                task=task,
                form=form,
                checklist_sections=checklist_sections,
                submitted_values=submitted_values,
                validation_errors=validation_errors,
            )

        # -----------------------------------------------------
        # Transaction 2:
        # Attempt delivery of the next task notification.
        # -----------------------------------------------------
        delivery_result = None

        try:
            delivery_result = (
                deliver_task_assignment_notification(
                    notification
                )
            )

            db.session.commit()

        except Exception:
            db.session.rollback()

            current_app.logger.exception(
                (
                    "The next workflow task was created, but its "
                    "notification delivery result could not be saved."
                )
            )

        # -----------------------------------------------------
        # User feedback
        # -----------------------------------------------------
        if (
            delivery_result is not None
            and delivery_result.success
        ):
            flash(
                (
                    f"Checklist submitted successfully with "
                    f"{response_count} responses. The workflow "
                    f"advanced to '{next_task.phase.name}', and "
                    "the next task notification was processed."
                ),
                "success",
            )

        else:
            flash(
                (
                    f"Checklist submitted successfully with "
                    f"{response_count} responses. The workflow "
                    f"advanced to '{next_task.phase.name}', but "
                    "the next task notification was not delivered "
                    "successfully."
                ),
                "warning",
            )

        return redirect(
            url_for(
                "workflow.view_task",
                task_id=task.id,
            )
        )

    return render_template(
        "workflow/task_detail.html",
        task=task,
        form=form,
        checklist_sections=checklist_sections,
        submitted_values=submitted_values,
        validation_errors=validation_errors,
    )