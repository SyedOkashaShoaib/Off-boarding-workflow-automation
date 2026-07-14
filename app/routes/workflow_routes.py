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


workflow_bp = Blueprint(
    "workflow",
    __name__,
    url_prefix="/workflow",
)


def build_checklist_sections(
    task: WorkflowTask,
) -> dict[str, list]:
    """
    Group active checklist items by their database section.
    """

    checklist_sections: dict[str, list] = {}

    for checklist_item in task.phase.checklist_items:
        if not checklist_item.is_active:
            continue

        section_name = (
            checklist_item.section
            or "Checklist"
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
    Convert saved ChecklistResponse records into values that the
    task template can display.
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


def record_task_opening(task: WorkflowTask) -> None:
    """
    Record only the first time the task is opened.

    A failure to save the opening timestamp does not prevent the
    task page from being displayed.
    """

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
                    "was not authenticated at this stage."
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
    Display and submit a database-driven workflow checklist.
    """

    task = WorkflowTask.query.get_or_404(task_id)

    record_task_opening(task)

    form = WorkflowChecklistForm()

    checklist_sections = build_checklist_sections(task)

    submitted_values = build_saved_response_values(task)
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
                    "Correct the highlighted items and submit again."
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

        try:
            response_count = persist_checklist_submission(
                task=task,
                submitted_values=submitted_values,
                responded_by=task.assigned_to_email,
            )

            db.session.commit()

        except ChecklistSubmissionError as exc:
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
                "Failed to submit workflow task %s.",
                task.id,
            )

            flash(
                (
                    "A database error occurred while submitting "
                    "the checklist. No responses were saved."
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

        flash(
            (
                f"Checklist submitted successfully with "
                f"{response_count} responses."
            ),
            "success",
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