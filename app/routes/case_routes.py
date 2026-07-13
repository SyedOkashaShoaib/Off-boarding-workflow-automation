from datetime import datetime

from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    url_for,
)
from sqlalchemy.exc import SQLAlchemyError

from app.extension import db
from app.forms.offboardingcaseform import CaseForm
from app.models import (
    EmailNotification,
    OffboardingCase,
    WorkflowTask,
)
from app.services.notification_service import (
    create_task_assignment_notification,
    deliver_task_assignment_notification,
)
from app.services.workflow_service import (
    WorkflowConfigurationError,
    create_initial_workflow_task,
)


case_bp = Blueprint("cases", __name__)


def generate_case_number() -> str:
    """
    Generate the next human-readable offboarding case number.

    Example:
        OFF-2026-0001
        OFF-2026-0002
    """
    current_year = datetime.now().year

    latest_case = (
        OffboardingCase.query
        .order_by(OffboardingCase.id.desc())
        .first()
    )

    next_number = 1 if latest_case is None else latest_case.id + 1

    return f"OFF-{current_year}-{next_number:04d}"


@case_bp.route("/create", methods=["GET", "POST"])
def create_case():
    """
    Create an offboarding case, its initial workflow task,
    and the first pending email-notification record.

    The database work is divided into two transactions:

    Transaction 1:
        - Create OffboardingCase
        - Create initial WorkflowTask
        - Create PENDING EmailNotification
        - Create initial audit logs

    Transaction 2:
        - Attempt notification delivery
        - Update notification to SENT or FAILED
        - Create delivery audit log
    """
    form = CaseForm()

    if not form.validate_on_submit():
        return render_template(
            "create_case.html",
            form=form,
        )

    # ---------------------------------------------------------
    # Transaction 1: Create the case and workflow records
    # ---------------------------------------------------------
    try:
        new_case = OffboardingCase(
            case_number=generate_case_number(),
            employee_name=form.emp_name.data.strip(),
            employee_id=form.emp_id.data.strip(),
            designation=form.emp_desig.data.strip(),
            department=form.emp_dep.data.strip(),
            last_working_day=form.last_date.data,
            line_manager=form.line_manager.data.strip(),
            status="CREATED",
            created_by="NOC",
        )

        db.session.add(new_case)

        initial_task = create_initial_workflow_task(
            new_case
        )

        notification = create_task_assignment_notification(
            initial_task
        )

        db.session.commit()

    except WorkflowConfigurationError as exc:
        db.session.rollback()

        flash(
            (
                "The offboarding case could not be started because "
                f"the workflow configuration is incomplete: {exc}"
            ),
            "error",
        )

        return render_template(
            "create_case.html",
            form=form,
        )

    except SQLAlchemyError:
        db.session.rollback()

        current_app.logger.exception(
            "Database error while creating an offboarding case."
        )

        flash(
            (
                "A database error occurred while creating the "
                "offboarding case. No case was saved."
            ),
            "error",
        )

        return render_template(
            "create_case.html",
            form=form,
        )

    # ---------------------------------------------------------
    # Transaction 2: Attempt email delivery
    # ---------------------------------------------------------
    delivery_result = None

    try:
        delivery_result = deliver_task_assignment_notification(
            notification
        )

        db.session.commit()

    except SQLAlchemyError:
        db.session.rollback()

        current_app.logger.exception(
            (
                "The notification was processed, but its delivery "
                "status could not be saved."
            )
        )

    # ---------------------------------------------------------
    # User feedback
    # ---------------------------------------------------------
    if delivery_result is not None and delivery_result.success:
        flash(
            (
                f"Offboarding case {new_case.case_number} was created "
                "successfully, and the initial task notification was "
                "processed."
            ),
            "success",
        )
    else:
        flash(
            (
                f"Offboarding case {new_case.case_number} was created "
                "successfully, but the task notification was not "
                "delivered successfully. It can be retried later."
            ),
            "warning",
        )

    return redirect(
        url_for(
            "cases.case_created",
            case_id=new_case.id,
        )
    )


@case_bp.route("/<int:case_id>/created")
def case_created(case_id):
    """
    Display the confirmation page after case creation.

    The page shows:
        - employee and case details;
        - initial workflow assignment;
        - notification delivery status;
        - configured email backend.
    """
    case = OffboardingCase.query.get_or_404(case_id)

    initial_task = (
        WorkflowTask.query
        .filter_by(case_id=case.id)
        .order_by(
            WorkflowTask.assigned_at.asc(),
            WorkflowTask.id.asc(),
        )
        .first_or_404()
    )

    notification = (
        EmailNotification.query
        .filter_by(
            workflow_task_id=initial_task.id,
            notification_type="TASK_ASSIGNED",
        )
        .order_by(EmailNotification.id.desc())
        .first()
    )

    return render_template(
        "case_created.html",
        case=case,
        task=initial_task,
        notification=notification,
        email_backend=current_app.config.get(
            "EMAIL_BACKEND",
            "console",
        ),
    )