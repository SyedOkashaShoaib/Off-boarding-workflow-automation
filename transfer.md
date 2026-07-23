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
"NO" : "No",
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
            {% set submission_response =
            task.response | first %}
            {% set submission_time =
            (task.submitted_at or submission_response.responded_at) %}
            {% set checklist_state.has_responses = true %}

            <section class="checklist-record">

                <div class="checklist-record__heading">

                    <div class="checklist-record__identity">
                        <h3>{{ task.phase.department.name }}</h3>
                        <p>{{ task.phase.name }}</p>
                    </div>


                    <dl class="checklist-record__metadata">

                        <div>
                            <dt>Submitted by</dt>

                            <dd>
                                {{
                                submission_response.responded_by
                                or task.assigned_to_email
                                or "Not recorded"
                                }}
                            </dd>
                        </div>


                        <div>
                            <dt>Submitted at</dt>

                            <dd>
                                {% if submission_time %}
                                {{
                                submission_time.strftime(
                                "%d %b %Y, %I:%M %p"
                                )
                                }}
                                {% else %}
                                Not recorded
                                {% endif %}
                            </dd>
                        </div>

                    </dl>


                    <span class="
        register-status
        register-status--task
        register-status--{{ task.status | lower }}
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

                        <colgroup>
                            <col class="checklist-record-table__item-column">
                            <col class="checklist-record-table__result-column">
                            <col class="checklist-record-table__reason-column">
                            <col class="checklist-record-table__employee-column">
                        </colgroup>

                        <thead>
                            <tr>
                                <th scope="col">Checklist Item</th>
                                <th scope="col">Result</th>
                                <th scope="col">Reason</th>
                                <th scope="col">Responsible Employee</th>
                            </tr>
                        </thead>

                        <tbody>

                            {% for response in task.responses
                            | sort(
                            attribute="checklist_item.display_order"
                            )
                            %}

                            {% set reason_text = (
                            response.response_reason
                            | default("", true)
                            | trim
                            ) %}

                            {% set responsible_employee = (
                            response.responsible_employee
                            ) %}

                            <tr>

                                <td>
                                    {% if response.checklist_item.section %}
                                    <span class="checklist-item-section">
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
                            response.response_status
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


                                <td class="checklist-reason-cell">

                                    {% if response.response_status == "YES" %}

                                    <span class="table-empty-value" aria-label="No reason required"
                                        title="No reason required">
                                        &mdash;
                                    </span>

                                    {% elif reason_text %}

                                    <span class="checklist-reason-text">
                                        {{ reason_text }}
                                    </span>

                                    {% else %}

                                    <span class="table-empty-value">
                                        Not recorded
                                    </span>

                                    {% endif %}

                                </td>


                                <td class="checklist-responsible-employee">

                                    {% if responsible_employee %}

                                    <strong class="
                                checklist-responsible-employee__name
                            ">
                                        {{ responsible_employee.full_name }}
                                    </strong>

                                    {% if responsible_employee.employee_code %}
                                    <span class="
                                    checklist-responsible-employee__code
                                ">
                                        {{
                                        responsible_employee
                                        .employee_code
                                        }}
                                    </span>
                                    {% endif %}

                                    {% else %}

                                    <span class="table-empty-value">
                                        Not recorded
                                    </span>

                                    {% endif %}

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
