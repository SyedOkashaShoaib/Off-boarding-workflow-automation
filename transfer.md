---detail.html---

{% extends "base.html" %}


{% block title %}
{{ record.case.case_number }} &middot; Case Details
{% endblock %}


{% block head %}
<link rel="stylesheet" href="{{ url_for(
            'static',
            filename='css/pages/cases.css'
        ) }}">
{% endblock %}


{% block breadcrumbs %}
<nav class="breadcrumbs" aria-label="Breadcrumb">
    <ol class="breadcrumbs__list">
        <li>Operations</li>

        <li>
            <a href="{{ url_for('cases.list_cases') }}">
                Cases
            </a>
        </li>

        <li aria-current="page">
            {{ record.case.case_number }}
        </li>
    </ol>
</nav>
{% endblock %}


{% block page_header %}

<div class="page-header">

    <div>
        <h1>{{ record.case.case_number }}</h1>

        <p>
            {{ record.case.employee_name }}
            &middot; Employee offboarding case
        </p>
    </div>


    <div class="case-detail-actions">

        <button type="button" class="btn-primary" data-print-case data-case-number="{{ record.case.case_number }}">
            Print Case
        </button>
        {% if reissue_task %}

        <a href="{{ url_for(
        'cases.reissue_task_access',
        case_id=record.case.id
    ) }}" class="
        btn-secondary
        case-reissue-action
    ">
            {% if reissue_task.phase.is_final_approval %}
            Reissue Approval Link
            {% else %}
            Reissue
            {{ reissue_task.phase.department.name }}
            Link
            {% endif %}
        </a>

        {% endif %}

        <a href="{{ url_for('cases.list_cases') }}" class="btn-secondary">
            Back to Cases
        </a>

    </div>

</div>

{% endblock %}


{% block content %}

{% set case_status_labels = {
"CREATED": "Created",
"IN_PROGRESS": "In Progress",
"CLOSED": "Closed"
} %}

{% set task_status_labels = {
"PENDING": "Pending",
"IN_PROGRESS": "In Progress",
"SUBMITTED": "Submitted",
"APPROVED": "Approved"
} %}

{% set response_status_labels = {
"YES": "Yes",
"NOT_APPLICABLE": "Not Applicable"
} %}

{% set audit_action_labels = {
"CASE_CREATED": "Case Created",
"TASK_CREATED": "Task Created",
"TASK_ASSIGNED": "Task Assigned",
"TASK_OPENED": "Task Opened",
"TASK_SUBMITTED": "Task Submitted",
"TASK_ACCESS_ACTIVATED": "Secure Access Activated",
"FINAL_APPROVAL_GRANTED": "Final Approval Granted",
"CASE_CLOSED": "Case Closed",
"TASK_ACCESS_REISSUE_REQUESTED": "Secure link Reissue Requested",
"TASK_ACCESS_REISSUE_SENT": "Replacement Secure Link Sent",
"TASK_ACCESS_REISSUE_FAILED": "Replacement Secure Link Failed",
} %}

<section class="case-print-header" aria-label="Printed case record heading">

    <div class="case-print-header__identity">

        <div>
            <strong class="case-print-header__company">
                Barrett Hodgson
            </strong>

            <span class="case-print-header__system">
                Offboarding Workflow System
            </span>
        </div>


        <div class="case-print-header__document">
            Employee Offboarding Case Record
        </div>

    </div>


    <dl class="case-print-header__metadata">

        <div>
            <dt>Case Number</dt>

            <dd>
                {{ record.case.case_number }}
            </dd>
        </div>


        <div>
            <dt>Employee</dt>

            <dd>
                {{ record.case.employee_name }}
            </dd>
        </div>


        <div>
            <dt>Employee ID</dt>

            <dd>
                {{ record.case.employee_id }}
            </dd>
        </div>


        <div>
            <dt>Record Printed</dt>

            <dd data-print-generated-at>
                Prepared for printing
            </dd>
        </div>

    </dl>

</section>


<!-- <div class="case-detail-page"> -->



<div class="case-detail-page">

    <!-- =====================================================
         Case information
         ===================================================== -->
    <section class="panel">

        <div class="panel__heading">
            <h2>Offboarding Case Information</h2>
        </div>

        <dl class="detail-grid">

            <div>
                <dt>Case Number</dt>
                <dd>{{ record.case.case_number }}</dd>
            </div>

            <div>
                <dt>Case Status</dt>

                <dd>
                    <span class="
                            register-status
                            register-status--case
                            register-status--{{ record.case.status | lower }}
                        ">
                        {{
                        case_status_labels.get(
                        record.case.status,
                        record.case.status
                        | replace("_", " ")
                        | title
                        )
                        }}
                    </span>
                </dd>
            </div>

            <div>
                <dt>Employee Name</dt>
                <dd>{{ record.case.employee_name }}</dd>
            </div>

            <div>
                <dt>Employee ID</dt>
                <dd>{{ record.case.employee_id }}</dd>
            </div>

            <div>
                <dt>Designation</dt>
                <dd>{{ record.case.designation }}</dd>
            </div>

            <div>
                <dt>Employee Department</dt>
                <dd>{{ record.case.department }}</dd>
            </div>

            <div>
                <dt>Line Manager</dt>
                <dd>{{ record.case.line_manager }}</dd>
            </div>

            <div>
                <dt>Last Working Day</dt>

                <dd>
                    {{
                    record.case.last_working_day.strftime(
                    "%d %B %Y"
                    )
                    }}
                </dd>
            </div>

            <div>
                <dt>Created By</dt>
                <dd>{{ record.case.created_by or "Not recorded" }}</dd>
            </div>

            <div>
                <dt>Created At</dt>

                <dd>
                    {{
                    record.case.created_at.strftime(
                    "%d %B %Y, %I:%M %p"
                    )
                    }}
                </dd>
            </div>

            <div>
                <dt>Last Updated</dt>

                <dd>
                    {{
                    record.case.updated_at.strftime(
                    "%d %B %Y, %I:%M %p"
                    )
                    }}
                </dd>
            </div>

            <div>
                <dt>Closed At</dt>

                <dd>
                    {% if record.case.closed_at %}
                    {{
                    record.case.closed_at.strftime(
                    "%d %B %Y, %I:%M %p"
                    )
                    }}
                    {% else %}
                    Not closed
                    {% endif %}
                </dd>
            </div>

        </dl>

    </section>


    <!-- =====================================================
         Current assignment
         ===================================================== -->
    <section class="panel">

        <div class="panel__heading">
            <h2>Current Assignment</h2>
        </div>

        {% if record.case.status == "CLOSED" %}

        <div class="case-detail-empty">
            <h3>Workflow Completed</h3>

            <p>
                This offboarding case is closed and has no active
                departmental assignment.
            </p>
        </div>

        {% elif record.current_task %}

        <dl class="detail-grid">

            <div>
                <dt>Current Phase</dt>
                <dd>{{ record.current_task.phase.name }}</dd>
            </div>

            <div>
                <dt>Responsible Department</dt>

                <dd>
                    {{
                    record.current_task.phase.department.name
                    }}
                </dd>
            </div>

            <div>
                <dt>Assigned Email</dt>
                <dd>{{ record.current_task.assigned_to_email }}</dd>
            </div>

            <div>
                <dt>Task Status</dt>

                <dd>
                    <span class="
                                register-status
                                register-status--task
                                register-status--{{
                                    record.current_task.status | lower
                                }}
                            ">
                        {{
                        task_status_labels.get(
                        record.current_task.status,
                        record.current_task.status
                        | replace("_", " ")
                        | title
                        )
                        }}
                    </span>
                </dd>
            </div>

            <div>
                <dt>Assigned At</dt>

                <dd>
                    {{
                    record.current_task.assigned_at.strftime(
                    "%d %B %Y, %I:%M %p"
                    )
                    }}
                </dd>
            </div>

            <div>
                <dt>Due At</dt>

                <dd>
                    {{
                    record.current_task.due_at.strftime(
                    "%d %B %Y, %I:%M %p"
                    )
                    }}
                </dd>
            </div>

            <div>
                <dt>Opened At</dt>

                <dd>
                    {% if record.current_task.opened_at %}
                    {{
                    record.current_task.opened_at.strftime(
                    "%d %B %Y, %I:%M %p"
                    )
                    }}
                    {% else %}
                    Not opened
                    {% endif %}
                </dd>
            </div>

            <div>
                <dt>Submitted At</dt>

                <dd>
                    {% if record.current_task.submitted_at %}
                    {{
                    record.current_task.submitted_at.strftime(
                    "%d %B %Y, %I:%M %p"
                    )
                    }}
                    {% else %}
                    Not submitted
                    {% endif %}
                </dd>
            </div>

        </dl>

        {% else %}

        <div class="case-detail-empty">
            <h3>No Current Assignment</h3>

            <p>
                No active workflow assignment is recorded for
                this case.
            </p>
        </div>

        {% endif %}

    </section>


    <!-- =====================================================
         Workflow history
         ===================================================== -->
    <section class="panel">

        <div class="panel__heading">
            <h2>Workflow History</h2>

            <p>
                Departmental assignments and completion activity
                recorded for this case.
            </p>
        </div>

        {% if record.tasks %}

        <div class="case-table-scroll" tabindex="0" role="region" aria-label="Case workflow history">
            <table class="case-register-table">

                <thead>
                    <tr>
                        <th scope="col">Phase</th>
                        <th scope="col">Department</th>
                        <th scope="col">Assigned To</th>
                        <th scope="col">Status</th>
                        <th scope="col">Assigned</th>
                        <th scope="col">Opened</th>
                        <th scope="col">Completed</th>
                    </tr>
                </thead>

                <tbody>
                    {% for task in record.tasks %}

                    <tr>

                        <td>
                            <strong>{{ task.phase.name }}</strong>
                        </td>

                        <td>
                            {{ task.phase.department.name }}
                        </td>

                        <td>
                            {{ task.assigned_to_email }}
                        </td>

                        <td>
                            <span class="
                                            register-status
                                            register-status--task
                                            register-status--{{
                                                task.status | lower
                                            }}
                                        ">
                                {{
                                task_status_labels.get(
                                task.status,
                                task.status
                                | replace("_", " ")
                                | title
                                )
                                }}
                            </span>
                        </td>

                        <td>
                            {{
                            task.assigned_at.strftime(
                            "%d %b %Y, %I:%M %p"
                            )
                            }}
                        </td>

                        <td>
                            {% if task.opened_at %}
                            {{
                            task.opened_at.strftime(
                            "%d %b %Y, %I:%M %p"
                            )
                            }}
                            {% else %}
                            <span class="table-empty-value">
                                Not opened
                            </span>
                            {% endif %}
                        </td>

                        <td>
                            {% if task.submitted_at %}
                            {{
                            task.submitted_at.strftime(
                            "%d %b %Y, %I:%M %p"
                            )
                            }}
                            {% else %}
                            <span class="table-empty-value">
                                Not completed
                            </span>
                            {% endif %}
                        </td>

                    </tr>

                    {% endfor %}
                </tbody>

            </table>
        </div>

        {% else %}

        <div class="case-detail-empty">
            <h3>No Workflow History</h3>

            <p>
                No workflow tasks have been created for this case.
            </p>
        </div>

        {% endif %}

    </section>


    <!-- =====================================================
         Checklist results
         ===================================================== -->
    <section class="panel case-detail-checklist-section">

        <div class="panel__heading">
            <h2>Departmental Checklist Results</h2>

            <p>
                Submitted checklist decisions recorded during the
                offboarding workflow.
            </p>
        </div>

        {% set checklist_state = namespace(has_responses=false) %}

        <div class="case-detail-checklists">

            {% for task in record.tasks %}

            {% if not task.phase.is_final_approval and task.responses %}

            {% set checklist_state.has_responses = true %}

            <section class="checklist-record">

                <div class="checklist-record__heading">

                    <div>
                        <h3>{{ task.phase.department.name }}</h3>
                        <p>{{ task.phase.name }}</p>
                    </div>

                    <span class="
                                    register-status
                                    register-status--task
                                    register-status--{{
                                        task.status | lower
                                    }}
                                ">
                        {{
                        task_status_labels.get(
                        task.status,
                        task.status
                        | replace("_", " ")
                        | title
                        )
                        }}
                    </span>

                </div>

                <div class="case-table-scroll" tabindex="0" role="region"
                    aria-label="{{ task.phase.name }} checklist results">
                    <table class="
                                    case-register-table
                                    checklist-record-table
                                ">

                        <thead>
                            <tr>
                                <th scope="col">Checklist Item</th>
                                <th scope="col">Result</th>
                                <th scope="col">N/A Reason</th>
                                <th scope="col">Responded By</th>
                                <th scope="col">Responded At</th>
                            </tr>
                        </thead>

                        <tbody>

                            {% for response in task.responses
                            | sort(
                            attribute="checklist_item.display_order"
                            )
                            %}

                            <tr>

                                <td>
                                    {% if response.checklist_item.section %}
                                    <span class="
                                                            checklist-item-section
                                                        ">
                                        {{
                                        response
                                        .checklist_item
                                        .section
                                        }}
                                    </span>
                                    {% endif %}

                                    <strong>
                                        {{
                                        response
                                        .checklist_item
                                        .item_text
                                        }}
                                    </strong>
                                </td>

                                <td>
                                    <span class="
                                                        checklist-result
                                                        checklist-result--{{
                                                            response
                                                            .response_status
                                                            | lower
                                                        }}
                                                    ">
                                        {{
                                        response_status_labels.get(
                                        response.response_status,
                                        response.response_status
                                        | replace("_", " ")
                                        | title
                                        )
                                        }}
                                    </span>
                                </td>

                                <td>
                                    {% if response.response_status
                                    == "NOT_APPLICABLE"
                                    %}
                                    {{
                                    response
                                    .not_applicable_reason
                                    or "No reason recorded"
                                    }}
                                    {% else %}
                                    <span class="
                                                            table-empty-value
                                                        ">
                                        Not applicable
                                    </span>
                                    {% endif %}
                                </td>

                                <td>
                                    {{
                                    response.responded_by
                                    or "Not recorded"
                                    }}
                                </td>

                                <td>
                                    {{
                                    response.responded_at.strftime(
                                    "%d %b %Y, %I:%M %p"
                                    )
                                    }}
                                </td>

                            </tr>

                            {% endfor %}

                        </tbody>

                    </table>
                </div>

            </section>

            {% endif %}

            {% endfor %}

        </div>

        {% if not checklist_state.has_responses %}

        <div class="case-detail-empty">
            <h3>No Checklist Results Recorded</h3>

            <p>
                Departmental checklist results will appear after
                a workflow task is submitted.
            </p>
        </div>

        {% endif %}

    </section>


    <!-- =====================================================
         Final approval
         ===================================================== -->
    <section class="panel">

        <div class="panel__heading">
            <h2>Final Approval</h2>

            <p>
                Administration approval and case-closure information.
            </p>
        </div>

        {% if record.final_task %}

        <dl class="detail-grid">

            <div>
                <dt>Approval Phase</dt>
                <dd>{{ record.final_task.phase.name }}</dd>
            </div>

            <div>
                <dt>Approval Status</dt>

                <dd>
                    <span class="
                                register-status
                                register-status--task
                                register-status--{{
                                    record.final_task.status | lower
                                }}
                            ">
                        {{
                        task_status_labels.get(
                        record.final_task.status,
                        record.final_task.status
                        | replace("_", " ")
                        | title
                        )
                        }}
                    </span>
                </dd>
            </div>

            <div>
                <dt>Assigned Approver</dt>
                <dd>{{ record.final_task.assigned_to_email }}</dd>
            </div>

            <div>
                <dt>Approved By</dt>

                <dd>
                    {% if record.final_approval_log %}
                    {{
                    record.final_approval_log.performed_by
                    or "Not recorded"
                    }}
                    {% else %}
                    Not yet approved
                    {% endif %}
                </dd>
            </div>

            <div>
                <dt>Approval Recorded At</dt>

                <dd>
                    {% if record.final_approval_log %}
                    {{
                    record.final_approval_log
                    .created_at.strftime(
                    "%d %B %Y, %I:%M %p"
                    )
                    }}
                    {% else %}
                    Not yet approved
                    {% endif %}
                </dd>
            </div>

            <div>
                <dt>Case Closed At</dt>

                <dd>
                    {% if record.case.closed_at %}
                    {{
                    record.case.closed_at.strftime(
                    "%d %B %Y, %I:%M %p"
                    )
                    }}
                    {% else %}
                    Case remains open
                    {% endif %}
                </dd>
            </div>

        </dl>

        {% if record.final_approval_log %}

        <div class="approval-record">
            <h3>Recorded Approval Details</h3>

            <p>
                {{
                record.final_approval_log.details
                or
                "No additional approval details were recorded."
                }}
            </p>
        </div>

        {% endif %}

        {% else %}

        <div class="case-detail-empty">
            <h3>Final Approval Not Yet Assigned</h3>

            <p>
                The Administration approval task will appear after
                the preceding departmental phases are completed.
            </p>
        </div>

        {% endif %}

    </section>


    <!-- =====================================================
         Operational activity
         ===================================================== -->
    <section class="panel case-detail-audit-section">

        <div class="panel__heading">
            <h2>Operational Activity</h2>

            <p>
                System and user actions recorded for this case.
            </p>
        </div>

        {% if record.audit_logs %}

        <ol class="audit-timeline">

            {% for audit_log in record.audit_logs %}

            <li class="audit-entry">

                <div class="audit-entry__marker" aria-hidden="true"></div>

                <div class="audit-entry__content">

                    <div class="audit-entry__heading">

                        <strong>
                            {{
                            audit_action_labels.get(
                            audit_log.action,
                            audit_log.action
                            | replace("_", " ")
                            | title
                            )
                            }}
                        </strong>

                        <time datetime="{{
                                        audit_log.created_at.isoformat()
                                    }}">
                            {{
                            audit_log.created_at.strftime(
                            "%d %b %Y, %I:%M %p"
                            )
                            }}
                        </time>

                    </div>

                    <p class="audit-entry__actor">
                        Performed by:
                        {{
                        audit_log.performed_by
                        or "System"
                        }}
                    </p>

                    {% if audit_log.details %}
                    <p class="audit-entry__details">
                        {{ audit_log.details }}
                    </p>
                    {% endif %}

                </div>

            </li>

            {% endfor %}

        </ol>

        {% else %}

        <div class="case-detail-empty">
            <h3>No Operational Activity Recorded</h3>

            <p>
                Audit events will appear as the case progresses.
            </p>
        </div>

        {% endif %}

    </section>

</div>

{% endblock %}

{% block scripts %}
<script src="{{url_for('static',filename='js/case_detail.js')}}" defer></script>
{% endblock %}


---case_routes.py---
from datetime import datetime

from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    url_for,
    request,
    abort,
)

from flask_login import (
    current_user,
    login_required,
)
from sqlalchemy.exc import SQLAlchemyError

from app.extension import db
from app.forms.offboarding_case import (
    Case_Form,
    )
from app.forms.case_action_forms import (
    ReissueTaskAccessForm,
)

from app.models import (
    EmailNotification,
    OffboardingCase,
    WorkflowTask,
    ROLE_NOC_OPERATOR,
    ROLE_SYSTEM_ADMIN,
)
from app.services.case_detail_service import (
    get_case_detail_record,
)
from app.services.notification_service import (
    create_task_assignment_notification,
    deliver_task_assignment_notification,
)
from app.services.workflow_service import (
    WorkflowConfigurationError,
    create_initial_workflow_task,
)

from app.services.case_query_service import (
    get_case_register_data
)
from app.services.task_access_reissue_service import (
    TaskAccessReissueError,
    get_reissuable_current_task,
    reissue_current_task_access,
)
case_bp = Blueprint("cases", __name__)

def require_case_operations_access()->None:
    if not current_user.has_role(
        ROLE_NOC_OPERATOR,
        ROLE_SYSTEM_ADMIN,
    ):
        abort(403)



@case_bp.get("/")
@login_required
def list_cases():
    register= get_case_register_data(request.args)
    return render_template('cases/index.html', register=register)
def generate_case_number() -> str:
    current_year = datetime.now().year

    latest_case = (
        OffboardingCase.query
        .order_by(OffboardingCase.id.desc())
        .first()
    )

    next_number = 1 if latest_case is None else latest_case.id + 1

    return f"OFF-{current_year}-{next_number:04d}"


@case_bp.route("/create", methods=["GET", "POST"])
@login_required
def create_case():
    form = Case_Form()

    if not form.validate_on_submit():
        return render_template(
            "create_case.html",
            form=form,
        )

    try:
        new_case = OffboardingCase(
            case_number=generate_case_number(),
            employee_name=form.emp_name.data.strip(),
            employee_id=form.emp_id.data,
            designation=form.emp_desig.data.strip(),
            department=form.emp_dep.data.strip(),
            last_working_day=form.last_date.data,
            line_manager=form.line_manager.data.strip(),
            status="CREATED",
            created_by=current_user.email,
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

    # if delivery_result is not None and delivery_result.success:
    #     # flash(
    #     #     (
    #     #         f"Offboarding case {new_case.case_number} was created "
    #     #         "successfully, and the initial task notification was "
    #     #         "processed."
    #     #     ),
    #     #     "success",
    #     # )
    #     pass
    # else:
    #     flash(
    #         (
    #             f"Offboarding case {new_case.case_number} was created "
    #             "successfully, but the task notification was not "
    #             "delivered successfully. It can be retried later."
    #         ),
    #         "warning",
    #     )

    return redirect(
        url_for(
            "cases.case_created",
            case_id=new_case.id,
        )
    )


@case_bp.route("/<int:case_id>/created")
@login_required
def case_created(case_id):
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

@case_bp.get("/<int:case_id>")
@login_required
def case_detail(case_id):
    """
    Display the complete read-only operational record for one
    offboarding case.
    """

    require_case_operations_access()

    record = get_case_detail_record(
        case_id
    )

    if record is None:
        abort(404)

    reissue_task = None

    try:
        reissue_task = (
            get_reissuable_current_task(
                record.case
            )
        )

    except TaskAccessReissueError:
        # An ineligible case remains viewable without a button.
        pass

    return render_template(
        "cases/detail.html",
        record=record,
        reissue_task=reissue_task,
    )

@case_bp.route(
    "/<int:case_id>/reissue-access",
    methods=["GET", "POST"],
)
@login_required
def reissue_task_access(case_id):
    """
    Confirm and execute replacement of the secure access link for
    the case's current eligible workflow task.
    """

    require_case_operations_access()

    case = OffboardingCase.query.get_or_404(
        case_id
    )

    try:
        task = get_reissuable_current_task(
            case
        )

    except TaskAccessReissueError as exc:
        flash(
            str(exc),
            "warning",
        )

        return redirect(
            url_for(
                "cases.case_detail",
                case_id=case.id,
            )
        )

    form = ReissueTaskAccessForm()

    if form.validate_on_submit():
        try:
            result = reissue_current_task_access(
                case=case,
                requested_by=current_user.email,
                reason=form.reason.data,
            )

            db.session.commit()

        except TaskAccessReissueError as exc:
            db.session.rollback()

            flash(
                str(exc),
                "error",
            )

            return redirect(
                url_for(
                    "cases.case_detail",
                    case_id=case.id,
                )
            )

        except SQLAlchemyError:
            db.session.rollback()

            current_app.logger.exception(
                (
                    "Database error while reissuing secure "
                    "task access for case %s."
                ),
                case.id,
            )

            flash(
                (
                    "The replacement-link request could not "
                    "be saved. No reliable reissue result "
                    "was recorded."
                ),
                "error",
            )

            return redirect(
                url_for(
                    "cases.case_detail",
                    case_id=case.id,
                )
            )

        if result.delivery_result.success:
            flash(
                (
                    "A replacement secure link for "
                    f"{result.task.phase.department.name} "
                    "was sent to "
                    f"{result.notification.recipient_email}. "
                    "All previous links and browser sessions "
                    "for this task are now invalid."
                ),
                "success",
            )

        else:
            flash(
                (
                    "All previous links for the current task "
                    "were invalidated, but the replacement "
                    "notification could not be delivered. "
                    "Check the recipient or email configuration "
                    "and reissue the link again."
                ),
                "warning",
            )

        return redirect(
            url_for(
                "cases.case_detail",
                case_id=case.id,
            )
        )
    if request.method=="POST":
        current_app.logger.warning("Secure link reissue form validation lowkey failed. %s", form.errors,)
        flash(
            (
                "The replacement link was not sent becuase"
             "the confirmation form contains validation errors"), "error",)
            
    return render_template(
        "cases/reissue_access.html",
        case=case,
        task=task,
        form=form,
    )


    ----cases.css---
    /* ============================================================
   Cases register
   ============================================================ */

.cases-page {
    max-width: 1500px;
}


.breadcrumbs {
    margin-bottom: 8px;
}


.breadcrumbs__list {
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
    margin: 0;
    padding: 0;
    color: var(--text-secondary);
    font-size: 12px;
    list-style: none;
}


.breadcrumbs__list li + li::before {
    margin-right: 6px;
    color: var(--text-muted);
    content: "›";
}


.cases-summary {
    display: grid;
    grid-template-columns:
        repeat(5, minmax(130px, 1fr));
    gap: 10px;
    margin-bottom: 18px;
}


.cases-summary-card {
    display: flex;
    min-height: 70px;
    justify-content: space-between;
    align-items: center;
    gap: 12px;
    padding: 12px 14px;
    color: #29485d;
    background:
        linear-gradient(
            to bottom,
            #ffffff,
            #e4edf4
        );
    border: 1px solid var(--border-medium);
    border-radius: var(--radius-medium);
    box-shadow:
        inset 0 1px 0 rgba(255, 255, 255, 0.95),
        0 1px 3px rgba(39, 69, 89, 0.14);
    text-decoration: none;
}


.cases-summary-card:hover {
    color: #173f5d;
    background:
        linear-gradient(
            to bottom,
            #ffffff,
            #d7e9f5
        );
    border-color: #6f96b0;
    text-decoration: none;
}


.cases-summary-card--current {
    background:
        linear-gradient(
            to bottom,
            #f9fdff,
            #cfe4f2
        );
    border-color: #4e83a6;
    box-shadow:
        inset 0 1px 0 rgba(255, 255, 255, 0.95),
        0 0 0 2px rgba(62, 126, 169, 0.12);
}


.cases-summary-card__label {
    font-size: 12px;
    font-weight: 600;
}


.cases-summary-card__value {
    color: #1e587f;
    font-size: 23px;
    line-height: 1;
}


.case-filter-panel,
.case-register-panel {
    margin-bottom: 18px;
    overflow: hidden;
    background: #ffffff;
    border: 1px solid var(--border-medium);
    border-radius: var(--radius-medium);
    box-shadow:
        inset 0 1px 0 rgba(255, 255, 255, 0.9),
        var(--shadow-panel);
}


.case-filter-panel__heading,
.case-register-panel__heading {
    padding: 10px 14px;
    background:
        linear-gradient(
            to bottom,
            #f9fcfe,
            #dce8f1
        );
    border-bottom: 1px solid var(--border-medium);
}


.case-filter-panel__heading h2,
.case-register-panel__heading h2 {
    margin: 0;
}


.case-filter-panel__heading p,
.case-register-panel__heading p {
    margin: 3px 0 0;
    color: var(--text-secondary);
    font-size: 12px;
}


.case-filter-form {
    display: grid;
    grid-template-columns:
        minmax(260px, 2fr)
        repeat(4, minmax(130px, 1fr))
        auto;
    align-items: end;
    gap: 12px;
    max-width: none;
    padding: 15px;
}


.case-filter-form > div {
    min-width: 0;
}


.case-filter-form label {
    display: block;
    margin-bottom: 5px;
    color: var(--text-secondary);
    font-size: 12px;
    font-weight: 600;
}


.case-filter-form input,
.case-filter-form select {
    width: 100%;
    min-height: 36px;
}


.case-filter-form__actions {
    display: flex;
    gap: 7px;
}


.case-table-scroll {
    overflow-x: auto;
    outline: none;
}


.case-table-scroll:focus-visible {
    outline: 2px solid #2e78a7;
    outline-offset: -2px;
}


.case-register-table {
    min-width: 1200px;
    margin: 0;
    border: 0;
    border-radius: 0;
}


.case-register-table th {
    white-space: nowrap;
}


.case-register-table td {
    font-size: 13px;
}


.case-number {
    color: #205f89;
    white-space: nowrap;
}


.table-secondary {
    display: block;
    margin-top: 3px;
    color: var(--text-secondary);
    font-size: 11px;
    line-height: 1.3;
}


.table-empty-value {
    color: var(--text-muted);
    font-style: italic;
}


.register-status,
.attention-indicator {
    display: inline-flex;
    min-height: 23px;
    align-items: center;
    padding: 2px 7px;
    border: 1px solid;
    border-radius: 10px;
    font-size: 11px;
    font-weight: 600;
    white-space: nowrap;
}


.register-status--created,
.register-status--pending {
    color: #4f5961;
    background: #edf1f4;
    border-color: #a4b0b8;
}


.register-status--in_progress {
    color: #245777;
    background: #e0eef7;
    border-color: #7d9fb6;
}


.register-status--submitted {
    color: #4c5d6a;
    background: #e8edf1;
    border-color: #9daab3;
}


.register-status--approved,
.register-status--closed {
    color: var(--success-text);
    background: var(--success-background);
    border-color: var(--success-border);
}


.attention-indicator--none {
    color: #536471;
    background: #eef2f4;
    border-color: #aab6be;
}


.attention-indicator--due_soon {
    color: var(--warning-text);
    background: var(--warning-background);
    border-color: var(--warning-border);
}


.attention-indicator--overdue,
.attention-indicator--workflow_issue {
    color: var(--error-text);
    background: var(--error-background);
    border-color: var(--error-border);
}


.attention-indicator--awaiting_approval {
    color: #315c7b;
    background: #e0edf6;
    border-color: #7c9db4;
}


.case-pagination {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 14px;
    padding: 12px 14px;
    background: #edf2f5;
    border-top: 1px solid var(--border-medium);
}


.case-pagination__summary {
    color: var(--text-secondary);
    font-size: 12px;
    font-weight: 600;
}


.case-pagination__controls {
    display: flex;
    gap: 7px;
}


.case-pagination [aria-disabled="true"] {
    opacity: 0.55;
    pointer-events: none;
}


.case-register-empty {
    padding: 34px 18px;
    text-align: center;
}


.case-register-empty h3 {
    margin: 0 0 6px;
}


.case-register-empty p {
    margin: 0 auto 15px;
    color: var(--text-secondary);
}


@media (max-width: 1150px) {

    .cases-summary {
        grid-template-columns:
            repeat(3, minmax(140px, 1fr));
    }


    .case-filter-form {
        grid-template-columns:
            repeat(3, minmax(150px, 1fr));
    }


    .case-filter-form__search {
        grid-column: span 2;
    }

}


@media (max-width: 720px) {

    .cases-summary {
        grid-template-columns:
            repeat(2, minmax(0, 1fr));
    }


    .case-filter-form {
        grid-template-columns: 1fr;
    }


    .case-filter-form__search {
        grid-column: auto;
    }


    .case-filter-form__actions {
        align-items: stretch;
        flex-direction: column;
    }


    .case-filter-form__actions > * {
        width: 100%;
    }


    .case-pagination {
        align-items: stretch;
        flex-direction: column;
    }


    .case-pagination__controls > * {
        flex: 1;
    }

}


@media (max-width: 430px) {

    .cases-summary {
        grid-template-columns: 1fr;
    }

}

/* ============================================================
   Case detail foundation
   ============================================================ */

.case-detail-page {
    display: grid;
    gap: 18px;
}


.detail-grid {
    display: grid;
    grid-template-columns:
        repeat(2, minmax(0, 1fr));
    gap: 14px 24px;
    margin: 0;
}


.detail-grid > div {
    padding-bottom: 10px;
    border-bottom: 1px solid var(--border-light);
}


.detail-grid dt {
    color: var(--text-secondary);
    font-size: 12px;
    font-weight: 600;
}


.detail-grid dd {
    margin: 4px 0 0;
    font-weight: 600;
    overflow-wrap: anywhere;
}


@media (max-width: 760px) {

    .detail-grid {
        grid-template-columns: 1fr;
    }

}

/* ============================================================ Case detail records ============================================================ */

.panel__heading p { margin: 3px 0 0; color: var(--text-secondary); font-size: 12px; }

.case-detail-checklists { display: grid; gap: 16px; }

.checklist-record { overflow: hidden; border: 1px solid var(--border-light); border-radius: var(--radius-medium); }

.checklist-record__heading { display: flex; align-items: center; justify-content: space-between; gap: 16px; padding: 10px 13px; background: #edf3f7; border-bottom: 1px solid var(--border-light); }

.checklist-record__heading h3 { margin: 0; font-size: 14px; }

.checklist-record__heading p { margin: 2px 0 0; color: var(--text-secondary); font-size: 12px; }

.checklist-record-table { min-width: 950px; }

.checklist-item-section { display: block; margin-bottom: 3px; color: var(--text-secondary); font-size: 11px; font-weight: 600; }

.checklist-result { display: inline-flex; min-height: 23px; align-items: center; padding: 2px 7px; border: 1px solid; border-radius: 10px; font-size: 11px; font-weight: 600; white-space: nowrap; }

.checklist-result--yes { color: var(--success-text); background: var(--success-background); border-color: var(--success-border); }

.checklist-result--not_applicable { color: #536471; background: #eef2f4; border-color: #aab6be; }

.approval-record { margin-top: 16px; padding: 13px 15px; background: #f5f8fa; border: 1px solid var(--border-light); border-radius: var(--radius-medium); }

.approval-record h3 { margin: 0 0 6px; font-size: 14px; }

.approval-record p { margin: 0; white-space: pre-line; }

.case-detail-empty { padding: 24px 18px; text-align: center; }

.case-detail-empty h3 { margin: 0 0 5px; }

.case-detail-empty p { margin: 0; color: var(--text-secondary); }

.audit-timeline { margin: 0; padding: 0; list-style: none; }

.audit-entry { display: grid; grid-template-columns: 14px minmax(0, 1fr); gap: 10px; position: relative; padding: 0 0 18px; }

.audit-entry:not(:last-child)::before { position: absolute; top: 12px; bottom: 0; left: 5px; width: 1px; background: var(--border-medium); content: ""; }

.audit-entry__marker { position: relative; z-index: 1; width: 11px; height: 11px; margin-top: 5px; background: #f7fbfd; border: 2px solid #5585a5; border-radius: 50%; }

.audit-entry__content { min-width: 0; padding-bottom: 2px; }

.audit-entry__heading { display: flex; align-items: baseline; justify-content: space-between; gap: 14px; }

.audit-entry__heading time { flex: none; color: var(--text-secondary); font-size: 11px; }

.audit-entry__actor { margin: 3px 0 0; color: var(--text-secondary); font-size: 12px; }

.audit-entry__details { margin: 6px 0 0; white-space: pre-line; overflow-wrap: anywhere; }

@media (max-width: 760px) {

.checklist-record__heading,
.audit-entry__heading {
    align-items: flex-start;
    flex-direction: column;
}

}

/* ============================================================ Case register navigation ============================================================ */

.case-number-link { display: inline-block; font-weight: 700; text-decoration: none; }

.case-number-link:hover { text-decoration: underline; }

.case-number-link:focus-visible { border-radius: 2px; outline: 2px solid #2e78a7; outline-offset: 2px; }

.case-register-row--clickable { cursor: pointer; }

.case-register-row--clickable:hover td { background: #f1f7fb; }

.case-register-row--clickable:focus-within td { background: #edf5fa; }

.case-register-table__action-column, .case-register-table__action-cell { width: 1%; text-align: right; white-space: nowrap; }

.case-register-view-link { display: inline-flex; min-height: 30px; align-items: center; justify-content: center; padding: 4px 10px; font-size: 12px; white-space: nowrap; }



/* ============================================================ Case printing controls ============================================================ */

.case-detail-actions { display: flex; align-items: center; justify-content: flex-end; flex-wrap: wrap; gap: 8px; }

.case-print-header { display: none; }

/* ============================================================ Printed case record ============================================================ */

@page { size: A4 portrait; margin: 12mm; }

@media print {

html,
body {
    width: auto;
    min-width: 0;
    margin: 0;
    padding: 0;
    color: #000;
    background: #fff;
    font-family: Arial, Helvetica, sans-serif;
    font-size: 9.5pt;
    line-height: 1.35;
}


*,
*::before,
*::after {
    box-shadow: none !important;
    text-shadow: none !important;
}


.skip-link,
.application-header,
.application-sidebar,
.page-context,
.system-messages,
.application-status-bar,
.case-detail-actions,
.case-detail-audit-section {
    display: none !important;
}


.application-shell,
.application-body,
.application-workspace,
.application-content {
    display: block !important;
    width: 100% !important;
    min-width: 0 !important;
    min-height: 0 !important;
    margin: 0 !important;
    padding: 0 !important;
    overflow: visible !important;
    color: #000 !important;
    background: #fff !important;
    border: 0 !important;
}


.case-print-header {
    display: block;
    margin: 0 0 7mm;
    padding: 0 0 4mm;
    border-bottom: 1.5px solid #000;
}


.case-print-header__identity {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: 8mm;
}


.case-print-header__company {
    display: block;
    font-size: 15pt;
    line-height: 1.15;
}


.case-print-header__system {
    display: block;
    margin-top: 1mm;
    font-size: 9pt;
}


.case-print-header__document {
    font-size: 12pt;
    font-weight: 700;
    text-align: right;
}


.case-print-header__metadata {
    display: grid;
    grid-template-columns:
        repeat(4, minmax(0, 1fr));
    gap: 3mm 6mm;
    margin: 5mm 0 0;
}


.case-print-header__metadata > div {
    min-width: 0;
}


.case-print-header__metadata dt {
    margin: 0;
    font-size: 7.5pt;
    font-weight: 700;
    text-transform: uppercase;
}


.case-print-header__metadata dd {
    margin: 1mm 0 0;
    font-weight: 600;
    overflow-wrap: anywhere;
}


.case-detail-page {
    display: block;
}


.case-detail-page > .panel {
    margin: 0 0 5mm;
    overflow: visible;
    background: #fff !important;
    border: 1px solid #777;
    border-radius: 0;
}


.panel__heading {
    padding: 2.5mm 3mm;
    color: #000 !important;
    background: #eee !important;
    border-bottom: 1px solid #777;
}


.panel__heading h2 {
    margin: 0;
    color: #000 !important;
    font-size: 11pt;
    break-after: avoid-page;
    page-break-after: avoid;
}


.panel__heading p {
    margin: 1mm 0 0;
    color: #222 !important;
    font-size: 8pt;
}


.detail-grid {
    grid-template-columns:
        repeat(2, minmax(0, 1fr));
    gap: 0;
    padding: 2mm 3mm;
}


.detail-grid > div {
    min-height: 11mm;
    padding: 2mm 3mm;
    border-bottom: 1px solid #ccc;
    break-inside: avoid;
    page-break-inside: avoid;
}


.detail-grid dt {
    color: #222 !important;
    font-size: 7.5pt;
}


.detail-grid dd {
    margin-top: 1mm;
    color: #000 !important;
    font-size: 9pt;
}


.case-detail-empty {
    padding: 4mm;
}


.case-detail-empty h3 {
    font-size: 10pt;
}


.case-detail-empty p {
    color: #222 !important;
}


.case-table-scroll {
    overflow: visible !important;
}


.case-register-table,
.checklist-record-table {
    width: 100% !important;
    min-width: 0 !important;
    table-layout: fixed;
    border-collapse: collapse;
}


.case-register-table thead {
    display: table-header-group;
}


.case-register-table tr {
    break-inside: avoid;
    page-break-inside: avoid;
}


.case-register-table th,
.case-register-table td {
    padding: 1.8mm;
    color: #000 !important;
    background: #fff !important;
    border: 1px solid #999;
    font-size: 7.5pt;
    line-height: 1.25;
    white-space: normal;
    overflow-wrap: anywhere;
}


.case-register-table th {
    background: #eee !important;
    font-weight: 700;
}


.checklist-record {
    margin: 0 3mm 4mm;
    overflow: visible;
    border: 1px solid #777;
    border-radius: 0;
}


.checklist-record__heading {
    padding: 2mm 3mm;
    background: #eee !important;
    border-bottom: 1px solid #777;
    break-after: avoid-page;
    page-break-after: avoid;
}


.checklist-record__heading h3 {
    color: #000 !important;
    font-size: 10pt;
}


.checklist-record__heading p {
    color: #222 !important;
}


.register-status,
.attention-indicator,
.checklist-result {
    min-height: 0;
    padding: 0;
    color: #000 !important;
    background: transparent !important;
    border: 0;
    border-radius: 0;
    font-size: inherit;
    font-weight: 600;
    white-space: normal;
}


.approval-record {
    margin: 3mm;
    padding: 3mm;
    color: #000 !important;
    background: #fff !important;
    border: 1px solid #999;
    border-radius: 0;
    break-inside: avoid;
    page-break-inside: avoid;
}


a,
a:visited {
    color: #000 !important;
    text-decoration: none !important;
}


h2,
h3,
thead {
    break-after: avoid-page;
    page-break-after: avoid;
}
/* Prevent the checklist collection being moved as one large grid. */ .case-detail-checklist-section, .case-detail-checklists, .checklist-record { display: block !important; }

.case-detail-checklist-section, .case-detail-checklists, .checklist-record, .checklist-record-table, .case-table-scroll { break-inside: auto !important; page-break-inside: auto !important; }

.case-detail-checklists { margin: 0; }

.checklist-record { margin: 0 3mm 4mm !important; overflow: visible !important; }

/*

    Keep each department heading with the beginning of its table,
    but allow the table itself to continue across pages. */ .checklist-record__heading { break-after: avoid-page !important; page-break-after: avoid !important; }

.checklist-record-table { display: table !important; width: 100% !important; }

.checklist-record-table thead { display: table-header-group; }

.checklist-record-table tbody { display: table-row-group; }

/* Individual checklist rows should normally remain intact. */ .checklist-record-table tr { break-inside: avoid !important; page-break-inside: avoid !important; }
}

/* ============================================================ Secure-link reissue ============================================================ */

.case-action-page { max-width: 900px; }

.reissue-warning { margin: 0 16px 18px; padding: 14px 16px; background: #fff7dc; border: 1px solid #c9a641; border-radius: var(--radius-medium); }

.reissue-warning h3 { margin: 0 0 5px; font-size: 14px; }

.reissue-warning p { margin: 0; line-height: 1.5; }

.case-action-summary { padding: 0 16px 16px; }

.case-action-form { padding: 16px; border-top: 1px solid var(--border-light); }

.case-action-field { display: grid; gap: 6px; }

.case-action-field__label { font-weight: 700; }

.case-action-field__help { margin: 0; color: var(--text-secondary); font-size: 12px; }

.case-action-field__textarea { width: 100%; min-height: 120px; resize: vertical; }

.case-action-field__errors { margin: 0; padding-left: 20px; color: #8b1e1e; font-size: 12px; }

.case-action-form__actions { display: flex; justify-content: flex-end; flex-wrap: wrap; gap: 8px; margin-top: 16px; }


---models.py---
from datetime import datetime, timedelta, timezone
from flask_login import UserMixin
from app.extension import db
from sqlalchemy.orm import validates
from werkzeug.security import (
    check_password_hash,
    generate_password_hash,
)


def utc_now():
    return datetime.now(timezone.utc)

ROLE_NOC_OPERATOR = "NOC_OPERATOR"
ROLE_FINAL_APPROVER = 'FINAL_APPROVER'
ROLE_SYSTEM_ADMIN = 'SYSTEM_ADMIN'

PORTAL_ROLES = (
    ROLE_NOC_OPERATOR,
    ROLE_FINAL_APPROVER,
    ROLE_SYSTEM_ADMIN,
)
class DepartmentEmployee(db.Model):
    """
    Employee available for selection as the person responsible
    for an individual departmental checklist item.
    """

    __tablename__ = "department_employees"

    __table_args__ = (
        db.Index(
            "ix_department_employees_department_active",
            "department_id",
            "is_active",
        ),
    )

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    department_id = db.Column(
        db.Integer,
        db.ForeignKey("departments.id"),
        nullable=False,
    )

    employee_code = db.Column(
        db.String(50),
        unique=True,
        nullable=False,
        index=True,
    )

    full_name = db.Column(
        db.String(150),
        nullable=False,
    )

    is_active = db.Column(
        db.Boolean,
        default=True,
        nullable=False,
    )

    department = db.relationship(
        "Department",
        back_populates="employees",
    )
    checklist_responses= db.relationship(
        "ChecklistResponse",
        back_populates='responsible_employee',
    )
    def __repr__(self):
        return (
            f"<DepartmentEmployee "
            f"{self.employee_code} "
            f"{self.full_name}>"
        )

class User(UserMixin, db.Model):
    """
    Authenticated portal user.

    Departmental task recipients will use separate task-specific
    access grants later and are not represented by this model unless
    they are also authorised portal users.
    """

    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    email = db.Column(
        db.String(254),
        unique=True,
        nullable=False,
        index=True,
    )

    full_name = db.Column(
        db.String(150),
        nullable=False,
    )

    password_hash = db.Column(
        db.String(512),
        nullable=False,
    )

    role = db.Column(
        db.String(50),
        nullable=False,
        default=ROLE_NOC_OPERATOR,
    )

    active = db.Column(
        db.Boolean,
        nullable=False,
        default=True,
    )

    last_login_at = db.Column(
        db.DateTime(timezone=True),
        nullable=True,
    )

    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=utc_now,
    )

    updated_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=utc_now,
        onupdate=utc_now,
    )

    @property
    def is_active(self) -> bool:
        """
        Flask-Login uses this property to determine whether the
        account is permitted to establish an authenticated session.
        """

        return bool(self.active)

    @staticmethod
    def normalize_email(value: str) -> str:
        """
        Return the canonical representation used for login and
        uniqueness checks.
        """

        return str(value or "").strip().lower()

    @validates("email")
    def validate_email(
        self,
        key: str,
        value: str,
    ) -> str:
        """
        Normalize portal email addresses before persistence.
        """

        normalized_email = self.normalize_email(value)

        if not normalized_email:
            raise ValueError(
                "A portal user email address is required."
            )

        return normalized_email

    @validates("role")
    def validate_role(
        self,
        key: str,
        value: str,
    ) -> str:
        """
        Reject unsupported portal roles.
        """

        normalized_role = str(value or "").strip().upper()

        if normalized_role not in PORTAL_ROLES:
            raise ValueError(
                f"Unsupported portal role: {normalized_role}"
            )

        return normalized_role

    def set_password(
        self,
        password: str,
    ) -> None:
        """
        Hash and store a plaintext password.

        Plaintext passwords must never be stored in the database.
        """

        if not password:
            raise ValueError(
                "A password is required."
            )

        self.password_hash = generate_password_hash(
            password
        )

    def check_password(
        self,
        password: str,
    ) -> bool:
        """
        Compare a submitted password with the stored hash.
        """

        if not password or not self.password_hash:
            return False

        return check_password_hash(
            self.password_hash,
            password,
        )

    def has_role(
        self,
        *roles: str,
    ) -> bool:
        """
        Return whether this user has one of the supplied roles.
        """

        normalized_roles = {
            str(role).strip().upper()
            for role in roles
        }

        return self.role in normalized_roles

    def __repr__(self) -> str:
        return (
            f"<User id={self.id} "
            f"email={self.email!r} "
            f"role={self.role!r}>"
        )
class Department(db.Model):
    __tablename__ = "departments"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(150), nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    phases = db.relationship("WorkflowPhase", back_populates="department")
    employees = db.relationship("DepartmentEmployee", back_populates='department', 
                                order_by='DepartmentEmployee.full_name', )

    def __repr__(self):
        return f"<Department {self.name}>"


class WorkflowPhase(db.Model):
    __tablename__ = "workflow_phases"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    slug = db.Column(db.String(100), unique=True, nullable=False)   

    department_id = db.Column(
        db.Integer,
        db.ForeignKey("departments.id"),
        nullable=False
    )

    phase_order = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=True)
    is_final_approval = db.Column(db.Boolean, default=False, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    department = db.relationship("Department", back_populates="phases")

    checklist_items = db.relationship(
        "ChecklistItem",
        back_populates="phase",
        order_by="ChecklistItem.display_order",
        cascade="all, delete-orphan"
    )

    tasks = db.relationship("WorkflowTask", back_populates="phase")

    def __repr__(self):
        return f"<WorkflowPhase {self.phase_order} - {self.name}>"


class ChecklistItem(db.Model):
    __tablename__ = "checklist_items"

    id = db.Column(db.Integer, primary_key=True)

    phase_id = db.Column(
        db.Integer,
        db.ForeignKey("workflow_phases.id"),
        nullable=False
    )

    section = db.Column(db.String(150), nullable=True)
    item_text = db.Column(db.Text, nullable=False)
    display_order = db.Column(db.Integer, nullable=False)

    is_required = db.Column(db.Boolean, default=True, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    phase = db.relationship("WorkflowPhase", back_populates="checklist_items")
    responses = db.relationship("ChecklistResponse", back_populates="checklist_item")

    def __repr__(self):
        return f"<ChecklistItem {self.item_text[:40]}>"


class OffboardingCase(db.Model):
    __tablename__ = "offboarding_cases"
    __table_args__=(
        db.Index(
        "ix_offboarding_case_status_updated_at",
        "status",
        "updated_at",
    ),
        db.Index(
            "ix_offboarding_case_current_phase_status",
            "current_phase_id",
            "status",
        ),
        db.Index(
            "ix_offboarding_case_employee_id",
            "employee_id",
        ),

    )
    id = db.Column(db.Integer, primary_key=True)

    case_number = db.Column(db.String(50), unique=True, nullable=False)

    employee_name = db.Column(db.String(150), nullable=False)
    employee_id = db.Column(db.String(50), nullable=False)

    designation = db.Column(db.String(150), nullable=False)
    department = db.Column(db.String(150), nullable=False)
    last_working_day = db.Column(db.Date, nullable=False)

    line_manager = db.Column(db.String(150), nullable=False)

    status = db.Column(db.String(50), nullable=False, default="CREATED")

    current_phase_id = db.Column(
        db.Integer,
        db.ForeignKey("workflow_phases.id"),
        nullable=True
    )

    created_by = db.Column(db.String(150), nullable=True)

    created_at = db.Column(
        db.DateTime(timezone=True),
        default=utc_now,
        nullable=False
    )

    updated_at = db.Column(
        db.DateTime(timezone=True),
        default=utc_now,
        onupdate=utc_now,
        nullable=False
    )

    closed_at = db.Column(db.DateTime(timezone=True), nullable=True)

    current_phase = db.relationship(
        "WorkflowPhase",
        foreign_keys=[current_phase_id]
    )

    tasks = db.relationship(
        "WorkflowTask",
        back_populates="case",
        cascade="all, delete-orphan"
    )

    audit_logs = db.relationship(
        "AuditLog",
        back_populates="case",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<OffboardingCase {self.case_number} - {self.employee_name}>"


class WorkflowTask(db.Model):
    __tablename__ = "workflow_tasks"
    __table_args__= (
        db.UniqueConstraint(
            "case_id",
            "phase_id",
            name="uq_workflow_tasks_case_phase",
        ),
        db.Index(
            "ix_workflow_tasks_status_due_at",
            "status",
            "due_at",
        ),
        
    )
    id = db.Column(db.Integer, primary_key=True)

    case_id = db.Column(
        db.Integer,
        db.ForeignKey("offboarding_cases.id"),
        nullable=False
    )

    phase_id = db.Column(
        db.Integer,
        db.ForeignKey("workflow_phases.id"),
        nullable=False
    )

    assigned_to_email = db.Column(db.String(150), nullable=False)
    status = db.Column(db.String(50), nullable=False, default="PENDING")

    assigned_at = db.Column(
        db.DateTime(timezone=True),
        default=utc_now,
        nullable=False
    )

    due_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: utc_now() + timedelta(days=7),
        nullable=False
    )

    opened_at = db.Column(db.DateTime(timezone=True), nullable=True)
    submitted_at = db.Column(db.DateTime(timezone=True), nullable=True)

    case = db.relationship("OffboardingCase", back_populates="tasks")
    phase = db.relationship("WorkflowPhase", back_populates="tasks")

    responses = db.relationship(
        "ChecklistResponse",
        back_populates="workflow_task",
        cascade="all, delete-orphan"
    )
    notifications= db.relationship(
        "EmailNotification", 
        back_populates='workflow_task', 
        cascade='all, delete-orphan')
    access_grants = db.relationship(
    "TaskAccessGrant",
    back_populates="workflow_task",
    cascade="all, delete-orphan",
)
    def __repr__(self):
        return f"<WorkflowTask Case={self.case_id} Phase={self.phase_id} Status={self.status}>"
class TaskAccessGrant(db.Model):
    """
    Secure access grant for one departmental workflow task.

    The raw token is sent through email but is never stored in the
    database. Only its SHA-256 digest is persisted.
    """

    __tablename__ = "task_access_grants"

    __table_args__ = (
        db.Index(
            "ix_task_access_grants_task_state",
            "workflow_task_id",
            "revoked_at",
            "consumed_at",
        ),
    )

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    workflow_task_id = db.Column(
        db.Integer,
        db.ForeignKey("workflow_tasks.id"),
        nullable=False,
    )

    token_hash = db.Column(
        db.String(64),
        unique=True,
        nullable=False,
    )

    recipient_email = db.Column(
        db.String(254),
        nullable=False,
    )

    expires_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
    )

    created_at = db.Column(
        db.DateTime(timezone=True),
        default=utc_now,
        nullable=False,
    )

    last_accessed_at = db.Column(
        db.DateTime(timezone=True),
        nullable=True,
    )

    access_count = db.Column(
        db.Integer,
        nullable=False,
        default=0,
    )

    consumed_at = db.Column(
        db.DateTime(timezone=True),
        nullable=True,
    )

    revoked_at = db.Column(
        db.DateTime(timezone=True),
        nullable=True,
    )

    workflow_task = db.relationship(
        "WorkflowTask",
        back_populates="access_grants",
    )

    def __repr__(self):
        return (
            f"<TaskAccessGrant id={self.id} "
            f"task={self.workflow_task_id}>"
        )

class ChecklistResponse(db.Model):
    """
    Recorded response for one checklist item within one workflow
    task.
    """

    __tablename__ = "checklist_responses"

    __table_args__ = (
        db.UniqueConstraint(
            "workflow_task_id",
            "checklist_item_id",
            name="uq_task_checklist_item_response",
        ),
    )

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    case_id = db.Column(
        db.Integer,
        db.ForeignKey("offboarding_cases.id"),
        nullable=False,
    )

    workflow_task_id = db.Column(
        db.Integer,
        db.ForeignKey("workflow_tasks.id"),
        nullable=False,
    )

    checklist_item_id = db.Column(
        db.Integer,
        db.ForeignKey("checklist_items.id"),
        nullable=False,
    )

    responsible_employee_id = db.Column(
        db.Integer,
        db.ForeignKey("department_employees.id"),
        nullable=False,
        index=True,
    )

    response_status = db.Column(
        db.String(50),
        nullable=False,
    )

    response_reason = db.Column(
        db.Text,
        nullable=True,
    )

    responded_by = db.Column(
        db.String(150),
        nullable=True,
    )

    responded_at = db.Column(
        db.DateTime(timezone=True),
        default=utc_now,
        nullable=False,
    )

    workflow_task = db.relationship(
        "WorkflowTask",
        back_populates="responses",
    )

    checklist_item = db.relationship(
        "ChecklistItem",
        back_populates="responses",
    )

    responsible_employee = db.relationship(
        "DepartmentEmployee",
        back_populates="checklist_responses",
    )

    @property
    def not_applicable_reason(self):
        """
        Temporary compatibility alias for checklist code that still
        refers to the previous field name.

        Remove this property after the checklist service and display
        code have been updated to use response_reason.
        """

        return self.response_reason

    @not_applicable_reason.setter
    def not_applicable_reason(
        self,
        value,
    ):
        self.response_reason = value

    def __repr__(self):
        return (
            f"<ChecklistResponse "
            f"Task={self.workflow_task_id} "
            f"Item={self.checklist_item_id}>"
        )


class AuditLog(db.Model):
    __tablename__ = "audit_logs"
    __table_args__ = (
        db.Index(
            "ix_audit_log_case_created_at",
            "case_id",
            "created_at",
        ),
    )
    id = db.Column(db.Integer, primary_key=True)

    case_id = db.Column(
        db.Integer,
        db.ForeignKey("offboarding_cases.id"),
        nullable=False
    )

    action = db.Column(db.String(150), nullable=False)
    performed_by = db.Column(db.String(150), nullable=True)
    details = db.Column(db.Text, nullable=True)

    created_at = db.Column(
        db.DateTime(timezone=True),
        default=utc_now,
        nullable=False
    )

    case = db.relationship("OffboardingCase", back_populates="audit_logs")

    def __repr__(self):
        return f"<AuditLog {self.action}>"
    

class EmailNotification(db.Model):
    __tablename__ = 'email_notifications'
    __table_args__=(
        db.Index("ix_email_notifications_case_status",
                 "case_id",
                 "status",),
        db.Index("ix_email_notifications_task_type",
                 "workflow_task_id",
                 "notification_type",),
    )
    id = db.Column(db.Integer, primary_key=True)
    case_id = db.Column(db.Integer, db.ForeignKey('offboarding_cases.id'), nullable=False)
    workflow_task_id = db.Column(db.Integer, db.ForeignKey('workflow_tasks.id'), nullable=False)
    notification_type = db.Column(db.String(50), nullable=False, default='TASK_ASSIGNED')
    deduplication_key = db.Column(db.String(255), unique= True, nullable=True)
    recipient_email = db.Column(db.String(150), nullable=False)
    subject = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(30), nullable=False, default='PENDING')
    provider_message_id = db.Column(db.String(255), nullable=True)
    error_message = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), default = utc_now, nullable=False)
    attempted_at = db.Column(db.DateTime(timezone=True), nullable=True)
    sent_at = db.Column(db.DateTime(timezone=True), nullable=True)
    case = db.relationship("OffboardingCase")
    workflow_task = db.relationship("WorkflowTask", back_populates='notifications')

    def __repr__(self):
        return (
            f"EmailNotification"
            f"Task={self.workflow_task_id}"
            f"Status={self.status}"
        )


