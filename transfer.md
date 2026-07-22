task detail.html

{% extends "layouts/task_base.html" %}


{% block title %}
    {{ task.case.case_number }} · Department Task
{% endblock %}


{% block head %}
    {{ super() }}
    <link rel="stylesheet" href = "{{url_for('static', filename='css/pages/task.css')}}">
{% endblock %}


{% block breadcrumbs %}
    <ol class="breadcrumbs">
        <li class="breadcrumbs__item">
            Operations
        </li>

        <li
            class="breadcrumbs__item breadcrumbs__item--current"
            aria-current="page"
        >
            Department Task
        </li>
    </ol>
{% endblock %}


{% block page_header %}
    <h1>Department Offboarding Task</h1>

    <p>
        Complete the assigned clearance checklist for
        {{ task.phase.department.name }}.
    </p>
{% endblock %}


{% block content %}
    {% set submitted = (
        task.submitted_at is not none
        or task.status in [
            "SUBMITTED",
            "COMPLETED",
            "APPROVED"
        ]
    ) %}

    {% set status_labels = {
        "PENDING": "Pending",
        "IN_PROGRESS": "In Progress",
        "SUBMITTED": "Submitted",
        "COMPLETED": "Completed",
        "APPROVED": "Approved"
    } %}

    {% set status_label = status_labels.get(
        task.status,
        task.status | replace("_", " ") | title
    ) %}


    <section class="task-summary-card">
        <div class="task-summary-card__case">
            <span class="task-summary-card__label">
                Case Number
            </span>

            <strong class="task-summary-card__case-number">
                {{ task.case.case_number }}
            </strong>
        </div>

        <div class="task-summary-card__main">
            <div>
                <p class="task-summary-card__eyebrow">
                    Workflow phase
                </p>

                <h2 class="task-summary-card__title">
                    {{ task.phase.name }}
                </h2>

                <p class="task-summary-card__department">
                    Responsible department:
                    <strong>
                        {{ task.phase.department.name }}
                    </strong>
                </p>
            </div>

            <span
                class="
                    status-badge
                    status-badge--{{
                        task.status
                        | lower
                        | replace('_', '-')
                    }}
                "
            >
                {{ status_label }}
            </span>
        </div>

        <dl class="task-summary-card__metadata">
            <div>
                <dt>Status</dt>
                <dd>{{ status_label }}</dd>
            </div>

            <div>
                <dt>Due Date</dt>
                <dd>
                    {% if task.due_at %}
                        {{ task.due_at.strftime(
                            "%d %B %Y, %I:%M %p"
                        ) }}
                    {% else %}
                        Not assigned
                    {% endif %}
                </dd>
            </div>
        </dl>
    </section>


    <section class="information-card">
        <header class="information-card__header">
            <h2>Employee Information</h2>
        </header>

        <dl class="information-grid">
            <div class="information-grid__item">
                <dt>Employee Name</dt>
                <dd>{{ task.case.employee_name }}</dd>
            </div>

            <div class="information-grid__item">
                <dt>Employee ID</dt>
                <dd>{{ task.case.employee_id }}</dd>
            </div>

            <div class="information-grid__item">
                <dt>Designation</dt>
                <dd>{{ task.case.designation }}</dd>
            </div>

            <div class="information-grid__item">
                <dt>Employee Department</dt>
                <dd>{{ task.case.department }}</dd>
            </div>

            <div class="information-grid__item">
                <dt>Line Manager</dt>
                <dd>{{ task.case.line_manager }}</dd>
            </div>

            <div class="information-grid__item">
                <dt>Last Working Day</dt>
                <dd>
                    {% if task.case.last_working_day %}
                        {{ task.case.last_working_day.strftime(
                            "%d %B %Y"
                        ) }}
                    {% else %}
                        Not recorded
                    {% endif %}
                </dd>
            </div>
        </dl>
    </section>


    {% if submitted %}
        <section
            class="task-alert task-alert--success"
            role="status"
        >
            <div class="task-alert__icon" aria-hidden="true">
                ✓
            </div>

            <div>
                <h2>Checklist Submitted</h2>

                {% if task.submitted_at %}
                    <p>
                        Your department’s clearance responses were
                        recorded successfully on
                        {{ task.submitted_at.strftime(
                            "%d %B %Y, %I:%M %p"
                        ) }}.
                    </p>
                {% else %}
                    <p>
                        Your department’s clearance responses were
                        recorded successfully.
                    </p>
                {% endif %}

                <p>
                    This task is now read-only.
                </p>
            </div>
        </section>
    {% endif %}


    {% if validation_errors %}
        <section
            class="validation-summary"
            role="alert"
            aria-labelledby="validation-summary-title"
        >
            <h2 id="validation-summary-title">
                Correct {{ validation_errors | length }}
                checklist
                {% if validation_errors | length == 1 %}
                    error
                {% else %}
                    errors
                {% endif %}
            </h2>

            <ul>
                {% for item_id, error_message
                    in validation_errors.items() %}
                    <li>
                        {{ error_message }}
                    </li>
                {% endfor %}
            </ul>
        </section>
    {% endif %}


    {% if form.csrf_token.errors %}
        <section
            class="validation-summary"
            role="alert"
        >
            <h2>Form security error</h2>

            <ul>
                {% for error in form.csrf_token.errors %}
                    <li>{{ error }}</li>
                {% endfor %}
            </ul>
        </section>
    {% endif %}


    {% if checklist_sections %}
        {% if not submitted %}
            <form
                method="post"
                class="checklist-form"
                data-checklist-form
            >
                {{ form.hidden_tag() }}
        {% endif %}


        {% if not submitted and not department_employees %}
            <div
                class="task-alert task-alert--error"
                role="alert"
            >
                <div>
                    <strong>
                        No responsible employees are available.
                    </strong>

                    <p>
                        This checklist cannot be submitted until at
                        least one active employee is configured for
                        {{ task.phase.department.name }}.
                    </p>
                </div>
            </div>
        {% endif %}


        <div class="checklist-sections">
            {% set item_counter = namespace(value=0) %}

            {% for section_name, checklist_items
                in checklist_sections.items() %}

                <section
                    class="checklist-section"
                    aria-labelledby="
                        checklist-section-{{ loop.index }}
                    "
                >
                    <header class="checklist-section__header">
                        <div>
                            <p class="checklist-section__eyebrow">
                                Checklist section
                            </p>

                            <h2
                                class="checklist-section__title"
                                id="checklist-section-{{ loop.index }}"
                            >
                                {{ section_name }}
                            </h2>
                        </div>

                        <span class="checklist-section__count">
                            {{ checklist_items | length }}

                            {% if checklist_items | length == 1 %}
                                item
                            {% else %}
                                items
                            {% endif %}
                        </span>
                    </header>


                    <div class="checklist-section__items">
                        {% for checklist_item
                            in checklist_items %}

                            {% set item_counter.value = (
                                item_counter.value + 1
                            ) %}

                            {% set saved_value = submitted_values.get(
                                checklist_item.id,
                                {}
                            ) %}

                            {% set selected_response = saved_value.get(
                                "response_status",
                                ""
                            ) %}

                            {% set saved_reason = saved_value.get(
                                "reason",
                                ""
                            ) %}

                            {% set selected_employee_id = (
                                saved_value.get(
                                    "responsible_employee_id",
                                    ""
                                )
                            ) %}

                            {% set item_error = validation_errors.get(
                                checklist_item.id
                            ) %}

                            {% set recorded_response = (
                                task.responses
                                | selectattr(
                                    "checklist_item_id",
                                    "equalto",
                                    checklist_item.id
                                )
                                | first
                            ) %}

                            {% set help_id = (
                                "checklist-help-"
                                ~ checklist_item.id
                            ) %}

                            {% set error_id = (
                                "checklist-error-"
                                ~ checklist_item.id
                            ) %}


                            <article
                                class="
                                    checklist-item
                                    {% if item_error %}
                                        checklist-item--invalid
                                    {% endif %}
                                "
                                data-checklist-item
                                data-item-id="{{ checklist_item.id }}"
                            >
                                <div class="checklist-item__heading">
                                    <div
                                        class="checklist-item__number"
                                        aria-hidden="true"
                                    >
                                        {{ item_counter.value }}
                                    </div>

                                    <div>
                                        <h3
                                            class="checklist-item__title"
                                        >
                                            {{ checklist_item.item_text }}
                                        </h3>

                                        {% if not submitted %}
                                            <span
                                                class="
                                                    checklist-item__required
                                                "
                                            >
                                                Response required
                                            </span>
                                        {% endif %}
                                    </div>
                                </div>


                                {% if submitted %}
                                    <div
                                        class="
                                            checklist-recorded-response
                                        "
                                    >
                                        <div
                                            class="
                                                checklist-recorded-response__item
                                            "
                                        >
                                            <span
                                                class="
                                                    checklist-recorded-response__label
                                                "
                                            >
                                                Recorded Response
                                            </span>

                                            <strong>
                                                {% if (
                                                    selected_response
                                                    == "YES"
                                                ) %}
                                                    Yes
                                                {% elif (
                                                    selected_response
                                                    == "NO"
                                                ) %}
                                                    No
                                                {% elif (
                                                    selected_response
                                                    == "NOT_APPLICABLE"
                                                ) %}
                                                    Not applicable
                                                {% else %}
                                                    Not recorded
                                                {% endif %}
                                            </strong>
                                        </div>


                                        <div
                                            class="
                                                checklist-recorded-response__item
                                            "
                                        >
                                            <span
                                                class="
                                                    checklist-recorded-response__label
                                                "
                                            >
                                                Responsible Employee
                                            </span>

                                            <strong>
                                                {% if (
                                                    recorded_response
                                                    and
                                                    recorded_response
                                                    .responsible_employee
                                                ) %}
                                                    {{
                                                        recorded_response
                                                        .responsible_employee
                                                        .full_name
                                                    }}

                                                    {% if (
                                                        recorded_response
                                                        .responsible_employee
                                                        .employee_code
                                                    ) %}
                                                        —
                                                        {{
                                                            recorded_response
                                                            .responsible_employee
                                                            .employee_code
                                                        }}
                                                    {% endif %}
                                                {% else %}
                                                    Not recorded
                                                {% endif %}
                                            </strong>
                                        </div>


                                        {% if selected_response in [
                                            "NO",
                                            "NOT_APPLICABLE"
                                        ] %}
                                            <div
                                                class="
                                                    checklist-recorded-response__item
                                                    checklist-recorded-response__item--full
                                                "
                                            >
                                                <span
                                                    class="
                                                        checklist-recorded-response__label
                                                    "
                                                >
                                                    Reason
                                                </span>

                                                <p>
                                                    {{
                                                        saved_reason
                                                        or
                                                        "No reason recorded."
                                                    }}
                                                </p>
                                            </div>
                                        {% endif %}
                                    </div>

                                {% else %}
                                    <div
                                        class="checklist-item__fields"
                                    >
                                        <fieldset
                                            class="response-fieldset"
                                            aria-describedby="{{ help_id }}{% if item_error %} {{ error_id }}{% endif %}"
                                        >
                                            <legend class="form-label">
                                                Response

                                                <span
                                                    class="required-marker"
                                                    aria-hidden="true"
                                                >
                                                    *
                                                </span>
                                            </legend>

                                            <p
                                                class="form-help"
                                                id="{{ help_id }}"
                                            >
                                                Select one response for
                                                this checklist item.
                                            </p>


                                            <div
                                                class="response-options"
                                                data-response-options
                                            >
                                                <label
                                                    class="
                                                        response-option
                                                        {% if (
                                                            selected_response
                                                            == "YES"
                                                        ) %}
                                                            response-option--selected
                                                        {% endif %}
                                                    "
                                                >
                                                    <input
                                                        type="radio"
                                                        name="response_{{ checklist_item.id }}"
                                                        value="YES"
                                                        data-response-option
                                                        required
                                                        {% if selected_response == "YES" %}
                                                            checked
                                                        {% endif %}
                                                    >

                                                    <span
                                                        class="
                                                            response-option__content
                                                        "
                                                    >
                                                        <strong>
                                                            Yes
                                                        </strong>

                                                        <small>
                                                            The required
                                                            action was
                                                            completed.
                                                        </small>
                                                    </span>
                                                </label>


                                                <label
                                                    class="
                                                        response-option
                                                        {% if (
                                                            selected_response
                                                            == "NO"
                                                        ) %}
                                                            response-option--selected
                                                        {% endif %}
                                                    "
                                                >
                                                    <input
                                                        type="radio"
                                                        name="response_{{ checklist_item.id }}"
                                                        value="NO"
                                                        data-response-option
                                                        required
                                                        {% if selected_response == "NO" %}
                                                            checked
                                                        {% endif %}
                                                    >

                                                    <span
                                                        class="
                                                            response-option__content
                                                        "
                                                    >
                                                        <strong>
                                                            No
                                                        </strong>

                                                        <small>
                                                            The required
                                                            action was not
                                                            completed.
                                                        </small>
                                                    </span>
                                                </label>


                                                <label
                                                    class="
                                                        response-option
                                                        {% if (
                                                            selected_response
                                                            == "NOT_APPLICABLE"
                                                        ) %}
                                                            response-option--selected
                                                        {% endif %}
                                                    "
                                                >
                                                    <input
                                                        type="radio"
                                                        name="response_{{ checklist_item.id }}"
                                                        value="NOT_APPLICABLE"
                                                        data-response-option
                                                        required
                                                        {% if selected_response == "NOT_APPLICABLE" %}
                                                            checked
                                                        {% endif %}
                                                    >

                                                    <span
                                                        class="
                                                            response-option__content
                                                        "
                                                    >
                                                        <strong>
                                                            Not applicable
                                                        </strong>

                                                        <small>
                                                            This action does
                                                            not apply.
                                                        </small>
                                                    </span>
                                                </label>
                                            </div>
                                        </fieldset>


                                        <div class="form-group">
                                            <label
                                                class="form-label"
                                                for="responsible-employee-{{ checklist_item.id }}"
                                            >
                                                Responsible employee

                                                <span
                                                    class="required-marker"
                                                    aria-hidden="true"
                                                >
                                                    *
                                                </span>
                                            </label>

                                            <select
                                                class="form-control"
                                                id="responsible-employee-{{ checklist_item.id }}"
                                                name="responsible_employee_{{ checklist_item.id }}"
                                                data-responsible-employee
                                                required
                                                {% if not department_employees %}
                                                    disabled
                                                {% endif %}
                                                {% if item_error %}
                                                    aria-invalid="true"
                                                    aria-describedby="{{ error_id }}"
                                                {% endif %}
                                            >
                                                <option value="">
                                                    Select an employee
                                                </option>

                                                {% for employee
                                                    in department_employees %}
                                                    <option
                                                        value="{{ employee.id }}"
                                                        {% if employee.id|string == selected_employee_id|string %}
                                                            selected
                                                        {% endif %}
                                                    >
                                                        {{ employee.full_name }}

                                                        {% if employee.employee_code %}
                                                            —
                                                            {{ employee.employee_code }}
                                                        {% endif %}
                                                    </option>
                                                {% endfor %}
                                            </select>

                                            <p class="form-help">
                                                Select the employee
                                                responsible for this
                                                individual checklist item.
                                            </p>
                                        </div>


                                        <div
                                            class="form-group reason-field"
                                            data-reason-container
                                            {% if selected_response not in [
                                                "NO",
                                                "NOT_APPLICABLE"
                                            ] %}
                                                hidden
                                            {% endif %}
                                        >
                                            <label
                                                class="form-label"
                                                for="response-reason-{{ checklist_item.id }}"
                                                data-reason-label
                                            >
                                                {% if selected_response == "NO" %}
                                                    Reason for No
                                                {% elif selected_response == "NOT_APPLICABLE" %}
                                                    Reason for Not applicable
                                                {% else %}
                                                    Reason or explanation
                                                {% endif %}
                                            </label>

                                            <textarea
                                                class="
                                                    form-control
                                                    form-control--textarea
                                                "
                                                id="response-reason-{{ checklist_item.id }}"
                                                name="reason_{{ checklist_item.id }}"
                                                rows="3"
                                                maxlength="2000"
                                                data-reason-input
                                                {% if selected_response in [
                                                    "NO",
                                                    "NOT_APPLICABLE"
                                                ] %}
                                                    required
                                                    aria-required="true"
                                                {% else %}
                                                    aria-required="false"
                                                {% endif %}
                                                {% if item_error %}
                                                    aria-invalid="true"
                                                    aria-describedby="{{ error_id }}"
                                                {% endif %}
                                            >{{ saved_reason }}</textarea>

                                            <p
                                                class="form-help"
                                                data-reason-hint
                                            >
                                                {% if selected_response == "NO" %}
                                                    Explain why the action
                                                    was not completed.
                                                {% elif selected_response == "NOT_APPLICABLE" %}
                                                    Explain why this action
                                                    does not apply.
                                                {% else %}
                                                    Required when the
                                                    response is No or Not
                                                    applicable.
                                                {% endif %}
                                            </p>
                                        </div>
                                    </div>


                                    {% if item_error %}
                                        <div
                                            class="
                                                checklist-item__error
                                            "
                                            id="{{ error_id }}"
                                            role="alert"
                                        >
                                            {{ item_error }}
                                        </div>
                                    {% endif %}
                                {% endif %}
                            </article>
                        {% endfor %}
                    </div>
                </section>
            {% endfor %}
        </div>


        {% if not submitted %}
            <section class="checklist-submit-panel">
                <div>
                    <h2>Submit Checklist</h2>

                    <p>
                        Review every response carefully. Submitting
                        this checklist advances the case to the next
                        workflow phase, and the responses cannot
                        currently be edited afterward.
                    </p>
                </div>

                {% if department_employees %}
                    {{ form.submit(
                        class_="btn-primary checklist-submit-button"
                    ) }}
                {% else %}
                    {{ form.submit(
                        class_="btn-primary checklist-submit-button",
                        disabled=True
                    ) }}
                {% endif %}
            </section>

            </form>
        {% endif %}

    {% else %}
        <section class="empty-state">
            <h2>Checklist Unavailable</h2>

            <p>
                No active checklist items are configured for this
                workflow phase. Contact the workflow administrator
                before continuing.
            </p>
        </section>
    {% endif %}


    <section class="assignment-details">
        <h2>Assignment Details</h2>

        <dl class="information-grid">
            <div class="information-grid__item">
                <dt>Assigned Email</dt>
                <dd>{{ task.assigned_to_email }}</dd>
            </div>

            <div class="information-grid__item">
                <dt>Assigned At</dt>
                <dd>
                    {% if task.assigned_at %}
                        {{ task.assigned_at.strftime(
                            "%d %B %Y, %I:%M %p"
                        ) }}
                    {% else %}
                        Not recorded
                    {% endif %}
                </dd>
            </div>

            <div class="information-grid__item">
                <dt>Opened At</dt>
                <dd>
                    {% if task.opened_at %}
                        {{ task.opened_at.strftime(
                            "%d %B %Y, %I:%M %p"
                        ) }}
                    {% else %}
                        Not recorded
                    {% endif %}
                </dd>
            </div>
        </dl>
    </section>
{% endblock %}


{% block scripts %}
    {{ super() }}

    {% if not submitted %}
        <script
            src="{{ url_for(
                'static',
                filename='js/task_checklist.js'
            ) }}"
            defer
        ></script>
    {% endif %}
{% endblock %}


---task base.html---
<!doctype html>

<html lang="en">

<head>
    <meta charset="utf-8">

    <meta
        name="viewport"
        content="width=device-width, initial-scale=1"
    >

    <title>
        {% block title %}
            Department Task
        {% endblock %}
    </title>

    <link
        rel="stylesheet"
        href="{{ url_for(
            'static',
            filename='css/app.css'
        ) }}"
    >

    <link
        rel="stylesheet"
        href="{{ url_for(
            'static',
            filename='css/pages/task_access.css'
        ) }}"
    >

    {% block head %}{% endblock %}
</head>


<body class="task-access-body">

    <a
        class="skip-link"
        href="#main-content"
    >
        Skip to main content
    </a>


    <header class="task-access-header">

        <div>
            <div class="task-access-header__company">
                Barrett Hodgson
            </div>

            <div class="task-access-header__system">
                Offboarding Workflow System
            </div>
        </div>

    </header>


    <main
        id="main-content"
        class="task-access-workspace"
    >

        {% with messages = get_flashed_messages(
            with_categories=true
        ) %}

            {% if messages %}
                <div aria-live="polite">
                    {% for category, message in messages %}
                        <div
                            class="
                                system-message
                                system-message--{{ category }}
                            "
                        >
                            {{ message }}
                        </div>
                    {% endfor %}
                </div>
            {% endif %}

        {% endwith %}


        {% block breadcrumbs %}{% endblock %}

        {% block page_header %}{% endblock %}

        {% block content %}{% endblock %}

    </main>


    <footer class="task-access-footer">
        Secure workflow task access
    </footer>

    {% block scripts %}{% endblock %}

</body>

</html>

----task_access.css ---

.task-access-body {
    min-height: 100vh;
    background: #dce7ef;
}


.task-access-header {
    padding: 13px 20px;
    color: #ffffff;
    background:
        linear-gradient(
            to bottom,
            var(--chrome-top),
            var(--chrome-bottom)
        );
    border-bottom: 1px solid #173e5a;
}


.task-access-header__company {
    font-size: 17px;
    font-weight: 600;
}


.task-access-header__system {
    margin-top: 2px;
    color: rgba(255, 255, 255, 0.82);
    font-size: 12px;
}


.task-access-workspace {
    width: min(1180px, calc(100% - 28px));
    margin: 20px auto;
}


.task-access-card {
    max-width: 620px;
    margin: 40px auto;
    padding: 20px;
    background: #ffffff;
    border: 1px solid var(--border-medium);
    border-radius: var(--radius-medium);
    box-shadow: var(--shadow-panel);
}


.task-access-card h1 {
    margin-top: 0;
}


.task-access-summary {
    display: grid;
    grid-template-columns:
        repeat(2, minmax(0, 1fr));
    gap: 12px 20px;
    margin: 18px 0;
}


.task-access-summary div {
    padding-bottom: 8px;
    border-bottom: 1px solid var(--border-light);
}


.task-access-summary dt {
    color: var(--text-secondary);
    font-size: 12px;
    font-weight: 600;
}


.task-access-summary dd {
    margin: 3px 0 0;
    font-weight: 600;
}


.task-access-warning {
    padding: 10px 12px;
    color: var(--warning-text);
    background: var(--warning-background);
    border: 1px solid var(--warning-border);
}


.task-access-footer {
    padding: 9px;
    color: #526875;
    font-size: 11px;
    text-align: center;
}


@media (max-width: 560px) {

    .task-access-summary {
        grid-template-columns: 1fr;
    }

}

---task.css---
/* ============================================================
   Department task interface
   ============================================================ */

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
    color: #7d8b95;
    content: "›";
}


.task-page-heading h1 {
    margin: 0 0 4px;
}


.task-page-heading p {
    margin: 0;
    color: var(--text-secondary);
}


.task-page {
    max-width: 1180px;
}


.task-hero {
    display: grid;
    grid-template-columns:
        minmax(0, 1fr)
        minmax(240px, 310px);
    gap: 24px;
    margin-bottom: 18px;
    padding: 20px;
    background:
        linear-gradient(
            to bottom,
            #ffffff,
            #edf5fa
        );
    border: 1px solid #7f9eb4;
    border-radius: var(--radius-medium);
    box-shadow:
        inset 0 1px 0 rgba(255, 255, 255, 0.95),
        0 2px 5px rgba(44, 75, 96, 0.14);
}


.task-hero__eyebrow {
    display: block;
    margin-bottom: 2px;
    color: var(--text-secondary);
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.06em;
    text-transform: uppercase;
}


.task-hero__case-number {
    display: block;
    margin-bottom: 9px;
    color: #1f5577;
    font-size: 15px;
}


.task-hero__phase {
    margin: 0 0 5px;
    color: #203d50;
    font-size: 21px;
}


.task-hero__department {
    margin: 0;
    color: var(--text-secondary);
}


.task-hero__status {
    display: grid;
    align-content: center;
    gap: 13px;
    margin: 0;
    padding-left: 22px;
    border-left: 1px solid #c7d5df;
}


.task-hero__status div {
    display: grid;
    grid-template-columns: 84px minmax(0, 1fr);
    gap: 10px;
}


.task-hero__status dt {
    color: var(--text-secondary);
    font-size: 12px;
    font-weight: 600;
}


.task-hero__status dd {
    margin: 0;
    font-weight: 600;
}


.task-status {
    display: inline-flex;
    min-height: 24px;
    align-items: center;
    padding: 2px 8px;
    color: #304a5c;
    background: #e7eef3;
    border: 1px solid #91a5b4;
    border-radius: 11px;
    font-size: 12px;
}


.task-status--in_progress {
    color: #234f71;
    background: #deedf8;
    border-color: #789fbc;
}


.task-status--submitted,
.task-status--approved {
    color: var(--success-text);
    background: var(--success-background);
    border-color: var(--success-border);
}


.task-panel {
    margin-bottom: 18px;
    overflow: hidden;
    background: #ffffff;
    border: 1px solid var(--border-medium);
    border-radius: var(--radius-medium);
    box-shadow: var(--shadow-panel);
}


.task-panel__heading {
    padding: 10px 14px;
    background:
        linear-gradient(
            to bottom,
            #f9fcfe,
            #dce8f1
        );
    border-bottom: 1px solid var(--border-medium);
}


.task-panel__heading h2 {
    margin: 0;
}


.task-panel__heading p {
    margin: 3px 0 0;
    color: var(--text-secondary);
    font-size: 12px;
}


.task-information-grid {
    display: grid;
    grid-template-columns:
        repeat(3, minmax(0, 1fr));
    margin: 0;
    padding: 16px;
    gap: 14px 24px;
}


.task-information-grid div {
    min-width: 0;
    padding-bottom: 8px;
    border-bottom: 1px solid #e2e9ee;
}


.task-information-grid dt {
    margin-bottom: 3px;
    color: var(--text-secondary);
    font-size: 12px;
    font-weight: 600;
}


.task-information-grid dd {
    margin: 0;
    overflow-wrap: anywhere;
    font-weight: 600;
}


/* .workflow-progress {
    display: grid;
    grid-template-columns:
        repeat(4, minmax(0, 1fr));
    margin: 0;
    padding: 19px 16px 20px;
    list-style: none;
}


.workflow-progress__item {
    position: relative;
    display: flex;
    align-items: flex-start;
    min-width: 0;
    gap: 9px;
}


.workflow-progress__item:not(:last-child)::after {
    position: absolute;
    z-index: 0;
    top: 14px;
    right: 8px;
    left: 38px;
    height: 2px;
    background: #bcc9d2;
    content: "";
}


.workflow-progress__item--completed:not(:last-child)::after {
    background: #699477;
}


.workflow-progress__marker {
    position: relative;
    z-index: 1;
    display: grid;
    flex: 0 0 29px;
    width: 29px;
    height: 29px;
    place-items: center;
    color: #526672;
    background:
        linear-gradient(
            to bottom,
            #ffffff,
            #dfe7ec
        );
    border: 1px solid #91a3b0;
    border-radius: 50%;
    font-size: 12px;
    font-weight: 700;
}


.workflow-progress__item--completed
.workflow-progress__marker {
    color: #ffffff;
    background:
        linear-gradient(
            to bottom,
            #6f9c7a,
            #477453
        );
    border-color: #3f694a;
}


.workflow-progress__item--current
.workflow-progress__marker {
    color: #ffffff;
    background:
        linear-gradient(
            to bottom,
            #5796c1,
            #27658f
        );
    border-color: #1f567d;
    box-shadow:
        0 0 0 3px rgba(70, 137, 181, 0.18);
}


.workflow-progress__content {
    position: relative;
    z-index: 1;
    display: flex;
    min-width: 0;
    padding-right: 10px;
    flex-direction: column;
    background: #ffffff;
}


.workflow-progress__content strong {
    overflow: hidden;
    color: #29465a;
    text-overflow: ellipsis;
    white-space: nowrap;
}


.workflow-progress__content span {
    color: var(--text-secondary);
    font-size: 11px;
} */


.task-submitted-panel {
    display: flex;
    align-items: flex-start;
    gap: 13px;
    margin-bottom: 18px;
    padding: 16px;
    color: var(--success-text);
    background: var(--success-background);
    border: 1px solid var(--success-border);
    border-radius: var(--radius-medium);
}


.task-submitted-panel__icon {
    display: grid;
    flex: 0 0 30px;
    width: 30px;
    height: 30px;
    place-items: center;
    color: #ffffff;
    background: #4d7d58;
    border-radius: 50%;
    font-weight: 700;
}


.task-submitted-panel h2 {
    margin: 1px 0 5px;
    color: inherit;
}


.task-submitted-panel p {
    margin: 3px 0;
}


.checklist-error-summary {
    margin-bottom: 18px;
    padding: 15px 17px;
    color: var(--error-text);
    background: var(--error-background);
    border: 1px solid var(--error-border);
    border-radius: var(--radius-medium);
}


.checklist-error-summary h2 {
    margin: 0 0 7px;
    color: inherit;
}


.checklist-error-summary ul {
    margin: 0;
    padding-left: 22px;
}


.checklist-error-summary a {
    color: inherit;
    font-weight: 600;
    text-decoration: underline;
}


.checklist-form {
    max-width: none;
}


.checklist-section {
    margin-bottom: 18px;
    overflow: hidden;
    background: #ffffff;
    border: 1px solid var(--border-medium);
    border-radius: var(--radius-medium);
    box-shadow: var(--shadow-panel);
}


.checklist-section__heading {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 16px;
    padding: 11px 14px;
    background:
        linear-gradient(
            to bottom,
            #f9fcfe,
            #dce8f1
        );
    border-bottom: 1px solid var(--border-medium);
}


.checklist-section__heading h2 {
    margin: 0;
}


.checklist-section__heading span {
    color: var(--text-secondary);
    font-size: 12px;
}


.checklist-section__items {
    padding: 0 16px;
}


.checklist-item {
    margin: 0;
    padding: 18px 0;
    outline: none;
}


.checklist-item + .checklist-item {
    border-top: 1px solid #dce4ea;
}


.checklist-item--error {
    margin: 0 -16px;
    padding-right: 16px;
    padding-left: 16px;
    background: #fff8f7;
    border-left: 4px solid var(--error-border);
}


.checklist-item__header {
    display: flex;
    align-items: flex-start;
    gap: 11px;
    margin-bottom: 13px;
}


.checklist-item__number {
    display: grid;
    flex: 0 0 27px;
    width: 27px;
    height: 27px;
    place-items: center;
    color: #294d65;
    background: #e3eef6;
    border: 1px solid #9cb5c7;
    border-radius: 50%;
    font-size: 12px;
    font-weight: 700;
}


.checklist-item__header h3 {
    margin: 1px 0 3px;
    color: #263d4d;
    font-size: 15px;
    line-height: 1.4;
}


.required-text {
    color: #805044;
    font-size: 11px;
    font-weight: 600;
}


.response-fieldset {
    margin: 0 0 13px 38px;
    padding: 0;
    background: transparent;
    border: 0;
    box-shadow: none;
}


.response-fieldset legend {
    margin-bottom: 7px;
    padding: 0;
    color: var(--text-secondary);
    font-size: 12px;
}


.response-options {
    display: grid;
    grid-template-columns:
        repeat(2, minmax(0, 280px));
    gap: 9px;
}


.response-option {
    display: flex;
    align-items: flex-start;
    min-height: 58px;
    gap: 8px;
    padding: 10px 11px;
    background:
        linear-gradient(
            to bottom,
            #ffffff,
            #f0f5f8
        );
    border: 1px solid #a4b5c1;
    border-radius: var(--radius-small);
    cursor: pointer;
}


.response-option:hover {
    background: #edf6fc;
    border-color: #6f99b6;
}


.response-option:has(input:checked) {
    background: #dceefa;
    border-color: #4d87ae;
    box-shadow:
        inset 0 1px 0 rgba(255, 255, 255, 0.9),
        0 0 0 1px rgba(61, 129, 174, 0.15);
}


.response-option input {
    margin-top: 2px;
}


.response-option span {
    display: flex;
    flex-direction: column;
}


.response-option small {
    margin-top: 2px;
    color: var(--text-secondary);
    font-weight: 400;
}


.not-applicable-reason {
    margin: 0 0 0 38px;
    padding: 12px;
    background: #f5f8fa;
    border: 1px solid #c6d2da;
    border-radius: var(--radius-small);
}


.not-applicable-reason.is-collapsed {
    display: none;
}


.field-help {
    margin: 2px 0 5px;
    color: var(--text-secondary);
    font-size: 12px;
}


.checklist-item__error {
    margin: 10px 0 0 38px;
    color: var(--error-text);
    font-weight: 600;
}


.recorded-response {
    margin-left: 38px;
    padding: 11px 13px;
    background: #f5f8fa;
    border: 1px solid #c7d3db;
    border-radius: var(--radius-small);
}


.recorded-response__label {
    display: block;
    margin-bottom: 3px;
    color: var(--text-secondary);
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
}


.recorded-reason {
    margin-top: 10px;
    padding-top: 9px;
    border-top: 1px solid #d6e0e6;
}


.recorded-reason span {
    color: var(--text-secondary);
    font-size: 12px;
    font-weight: 600;
}


.recorded-reason p {
    margin: 3px 0 0;
}


.checklist-actions {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 22px;
    margin-top: 20px;
    padding: 16px;
    background:
        linear-gradient(
            to bottom,
            #f9fbfc,
            #e3ebf0
        );
    border: 1px solid var(--border-medium);
    border-radius: var(--radius-medium);
}


.checklist-actions p {
    margin: 0;
    color: var(--text-secondary);
}


.checklist-submit-button {
    flex: 0 0 auto;
}


.confirmation-dialog {
    width: min(480px, calc(100vw - 32px));
    padding: 0;
    color: var(--text-primary);
    background: #f5f8fa;
    border: 1px solid #496c84;
    border-radius: var(--radius-medium);
    box-shadow:
        0 14px 40px rgba(17, 38, 54, 0.38);
}


.confirmation-dialog::backdrop {
    background: rgba(25, 43, 56, 0.46);
}


.confirmation-dialog__titlebar {
    padding: 10px 13px;
    color: #ffffff;
    background:
        linear-gradient(
            to bottom,
            var(--chrome-top),
            var(--chrome-bottom)
        );
    border-bottom: 1px solid #244d68;
}


.confirmation-dialog__titlebar h2 {
    margin: 0;
    color: inherit;
    font-size: 16px;
}


.confirmation-dialog__content {
    padding: 17px;
}


.confirmation-dialog__content p {
    margin: 0 0 9px;
}


.confirmation-dialog__actions {
    display: flex;
    justify-content: flex-end;
    gap: 9px;
    padding: 12px 15px;
    background: #e8eef2;
    border-top: 1px solid #b6c4ce;
}


.task-empty-state {
    padding: 20px;
    color: var(--error-text);
    background: var(--error-background);
    border: 1px solid var(--error-border);
    border-radius: var(--radius-medium);
}


.task-empty-state h2 {
    color: inherit;
}


.task-technical-details {
    margin-top: 18px;
    background: #f3f7f9;
    border: 1px solid #b7c5cf;
    border-radius: var(--radius-small);
}


.task-technical-details summary {
    padding: 9px 12px;
    color: #31536a;
    font-weight: 600;
    cursor: pointer;
}


.task-technical-details dl {
    display: grid;
    grid-template-columns:
        repeat(3, minmax(0, 1fr));
    gap: 13px 20px;
    margin: 0;
    padding: 13px;
    border-top: 1px solid #c8d3db;
}


.task-technical-details dt {
    color: var(--text-secondary);
    font-size: 12px;
    font-weight: 600;
}


.task-technical-details dd {
    margin: 2px 0 0;
    overflow-wrap: anywhere;
}


@media (max-width: 850px) {

    .task-hero {
        grid-template-columns: 1fr;
    }


    .task-hero__status {
        padding-top: 15px;
        padding-left: 0;
        border-top: 1px solid #c7d5df;
        border-left: 0;
    }


    .task-information-grid {
        grid-template-columns:
            repeat(2, minmax(0, 1fr));
    }


    /* .workflow-progress {
        grid-template-columns: 1fr;
        gap: 10px;
    }


    .workflow-progress__item:not(:last-child)::after {
        top: 29px;
        right: auto;
        bottom: -11px;
        left: 14px;
        width: 2px;
        height: auto;
    }


    .workflow-progress__content {
        background: transparent;
    } */


    .checklist-actions {
        align-items: stretch;
        flex-direction: column;
    }

}


@media (max-width: 560px) {

    .task-information-grid,
    .response-options,
    .task-technical-details dl {
        grid-template-columns: 1fr;
    }


    .task-hero__status div {
        grid-template-columns: 1fr;
        gap: 2px;
    }


    .response-fieldset,
    .not-applicable-reason,
    .checklist-item__error,
    .recorded-response {
        margin-left: 0;
    }


    .checklist-item__header {
        gap: 8px;
    }


    .confirmation-dialog__actions {
        align-items: stretch;
        flex-direction: column-reverse;
    }


    .confirmation-dialog__actions button {
        width: 100%;
    }

}

.checklist-sections {
    display: grid;
    gap: 1.5rem;
}

.checklist-section {
    overflow: hidden;
    border: 1px solid #b8c4cf;
    border-radius: 8px;
    background: #ffffff;
    box-shadow:
        0 1px 2px rgba(30, 45, 60, 0.08),
        0 8px 20px rgba(30, 45, 60, 0.05);
}

.checklist-section__header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1rem;
    padding: 1rem 1.25rem;
    border-bottom: 1px solid #cbd4dc;
    background:
        linear-gradient(
            180deg,
            #f8fbfd 0%,
            #e7edf2 100%
        );
}

.checklist-section__eyebrow {
    margin: 0 0 0.2rem;
    color: #526576;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.06em;
    text-transform: uppercase;
}

.checklist-section__title {
    margin: 0;
    color: #1f2f3d;
    font-size: 1.1rem;
}

.checklist-section__count {
    flex: 0 0 auto;
    padding: 0.3rem 0.65rem;
    border: 1px solid #aebbc6;
    border-radius: 999px;
    background: #ffffff;
    color: #3f5364;
    font-size: 0.8rem;
    font-weight: 700;
}

.checklist-section__items {
    display: grid;
}

.checklist-item {
    padding: 1.25rem;
    border-bottom: 1px solid #d8e0e6;
}

.checklist-item:last-child {
    border-bottom: 0;
}

.checklist-item--invalid {
    background: #fff9f8;
    box-shadow:
        inset 4px 0 0 #a13a32;
}

.checklist-item__heading {
    display: grid;
    grid-template-columns: auto minmax(0, 1fr);
    gap: 0.75rem;
    align-items: start;
    margin-bottom: 1rem;
}

.checklist-item__number {
    display: grid;
    width: 1.8rem;
    height: 1.8rem;
    place-items: center;
    border: 1px solid #9fadb9;
    border-radius: 50%;
    background:
        linear-gradient(
            180deg,
            #ffffff 0%,
            #e4ebf0 100%
        );
    color: #2f4353;
    font-size: 0.8rem;
    font-weight: 700;
}

.checklist-item__title {
    margin: 0;
    color: #172734;
    font-size: 1rem;
    line-height: 1.45;
}

.checklist-item__description {
    margin: 0.35rem 0 0;
    color: #566a7a;
    font-size: 0.9rem;
    line-height: 1.5;
}

.checklist-item__fields {
    display: grid;
    grid-template-columns:
        minmax(18rem, 1.3fr)
        minmax(13rem, 0.8fr);
    gap: 1rem;
    align-items: start;
}

.response-fieldset {
    min-width: 0;
    margin: 0;
    padding: 0;
    border: 0;
}

.response-options {
    display: grid;
    grid-template-columns: repeat(
        3,
        minmax(0, 1fr)
    );
    gap: 0.65rem;
}

.response-option {
    position: relative;
    display: block;
    min-width: 0;
    cursor: pointer;
}

.response-option input {
    position: absolute;
    width: 1px;
    height: 1px;
    overflow: hidden;
    opacity: 0;
    pointer-events: none;
}

.response-option__content {
    display: grid;
    gap: 0.2rem;
    height: 100%;
    padding: 0.75rem;
    border: 1px solid #aebbc6;
    border-radius: 6px;
    background:
        linear-gradient(
            180deg,
            #ffffff 0%,
            #edf2f5 100%
        );
    color: #263b4b;
    transition:
        border-color 120ms ease,
        box-shadow 120ms ease,
        transform 120ms ease;
}

.response-option__content strong {
    font-size: 0.9rem;
}

.response-option__content small {
    color: #5b6e7d;
    font-size: 0.78rem;
    line-height: 1.35;
}

.response-option:hover
.response-option__content {
    border-color: #738da2;
}

.response-option input:focus-visible
+ .response-option__content {
    outline: 3px solid rgba(43, 105, 155, 0.25);
    outline-offset: 2px;
}

.response-option--selected
.response-option__content {
    border-color: #356f9e;
    background:
        linear-gradient(
            180deg,
            #f7fcff 0%,
            #dcebf6 100%
        );
    box-shadow:
        inset 0 0 0 1px #75a6c8,
        0 2px 5px rgba(37, 77, 108, 0.12);
    transform: translateY(-1px);
}

.response-option input:disabled
+ .response-option__content {
    cursor: default;
    opacity: 0.75;
}

.form-group {
    min-width: 0;
}

.form-label {
    display: block;
    margin-bottom: 0.4rem;
    color: #233746;
    font-size: 0.88rem;
    font-weight: 700;
}

.required-marker {
    color: #8d2d27;
}

.form-control {
    box-sizing: border-box;
    width: 100%;
    min-height: 2.5rem;
    padding: 0.6rem 0.7rem;
    border: 1px solid #9eacb8;
    border-radius: 5px;
    background: #ffffff;
    color: #1d2d39;
    font: inherit;
}

.form-control:focus {
    border-color: #3977a7;
    outline: 3px solid rgba(57, 119, 167, 0.18);
}

.form-control[aria-invalid="true"] {
    border-color: #9d3932;
}

.form-control--textarea {
    min-height: 5.5rem;
    resize: vertical;
}

.form-help {
    margin: 0.35rem 0 0;
    color: #657684;
    font-size: 0.78rem;
    line-height: 1.4;
}

.reason-field {
    grid-column: 1 / -1;
    max-width: 50rem;
}

.reason-field[hidden] {
    display: none;
}

.checklist-item__error {
    margin-top: 1rem;
    padding: 0.7rem 0.8rem;
    border: 1px solid #c89792;
    border-radius: 5px;
    background: #fff1ef;
    color: #762b26;
    font-size: 0.85rem;
    font-weight: 600;
}

.task-alert {
    margin-bottom: 1rem;
    padding: 0.9rem 1rem;
    border-radius: 6px;
}

.task-alert p {
    margin: 0.35rem 0 0;
}

.task-alert--error {
    border: 1px solid #c89792;
    background: #fff1ef;
    color: #762b26;
}

@media (max-width: 900px) {
    .checklist-item__fields {
        grid-template-columns: 1fr;
    }

    .response-options {
        grid-template-columns: 1fr;
    }

    .reason-field {
        grid-column: auto;
    }
}

