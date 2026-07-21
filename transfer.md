{% extends "base.html" %}


{% block title %}
    Reissue Secure Link &middot; {{ case.case_number }}
{% endblock %}


{% block head %}
    <link
        rel="stylesheet"
        href="{{ url_for(
            'static',
            filename='css/pages/cases.css'
        ) }}"
    >
{% endblock %}


{% block breadcrumbs %}
    <nav
        class="breadcrumbs"
        aria-label="Breadcrumb"
    >
        <ol class="breadcrumbs__list">

            <li>
                Operations
            </li>

            <li>
                <a href="{{ url_for('cases.list_cases') }}">
                    Cases
                </a>
            </li>

            <li>
                <a
                    href="{{ url_for(
                        'cases.case_detail',
                        case_id=case.id
                    ) }}"
                >
                    {{ case.case_number }}
                </a>
            </li>

            <li aria-current="page">
                Reissue Secure Link
            </li>

        </ol>
    </nav>
{% endblock %}


{% block page_header %}
    <div class="page-header">

        <div>
            <h1>Reissue Secure Link</h1>

            <p>
                {{ case.case_number }}
                &middot;
                {{ task.phase.department.name }}
            </p>
        </div>

        <a
            href="{{ url_for(
                'cases.case_detail',
                case_id=case.id
            ) }}"
            class="btn-secondary"
        >
            Cancel
        </a>

    </div>
{% endblock %}


{% block content %}

<div class="case-action-page">

    <section class="panel">

        <div class="panel__heading">

            <h2>Confirm Replacement Access</h2>

            <p>
                Review the current assignment before issuing
                a replacement secure link.
            </p>

        </div>


        <div class="reissue-warning">

            <h3>Previous access will be invalidated</h3>

            <p>
                Reissuing this link will revoke every previously
                issued secure link and invalidate any browser
                session currently authorised for this task.
            </p>

        </div>


        <dl class="detail-grid case-action-summary">

            <div>
                <dt>Case Number</dt>

                <dd>
                    {{ case.case_number }}
                </dd>
            </div>


            <div>
                <dt>Employee</dt>

                <dd>
                    {{ case.employee_name }}
                </dd>
            </div>


            <div>
                <dt>Employee ID</dt>

                <dd>
                    {{ case.employee_id }}
                </dd>
            </div>


            <div>
                <dt>Current Phase</dt>

                <dd>
                    {{ task.phase.name }}
                </dd>
            </div>


            <div>
                <dt>Department</dt>

                <dd>
                    {{ task.phase.department.name }}
                </dd>
            </div>


            <div>
                <dt>Recipient</dt>

                <dd>
                    {{ task.assigned_to_email }}
                </dd>
            </div>


            <div>
                <dt>Task Status</dt>

                <dd>
                    {{
                        task.status
                        | replace("_", " ")
                        | title
                    }}
                </dd>
            </div>


            <div>
                <dt>Due Date</dt>

                <dd>
                    {% if task.due_at %}
                        {{
                            task.due_at.strftime(
                                "%d %b %Y, %I:%M %p"
                            )
                        }}
                    {% else %}
                        Not specified
                    {% endif %}
                </dd>
            </div>

        </dl>


        <form
            method="post"
            action="{{ url_for(
                'cases.reissue_task_access',
                case_id=case.id
            ) }}"
            class="case-action-form"
        >

            {{ form.hidden_tag() }}


            {% if form.csrf_token.errors %}

                <div
                    class="system-message system-message--error"
                    role="alert"
                >
                    <div>
                        <strong>
                            The replacement link was not sent.
                        </strong>

                        <ul>
                            {% for error in form.csrf_token.errors %}
                                <li>{{ error }}</li>
                            {% endfor %}
                        </ul>
                    </div>
                </div>

            {% endif %}


            <div class="case-action-field">

                {{
                    form.reason.label(
                        class_="case-action-field__label"
                    )
                }}

                <p
                    id="reissue-reason-help"
                    class="case-action-field__help"
                >
                    Record the operational reason for replacing
                    the existing link. This reason will be retained
                    in the case audit trail.
                </p>

                {{
                    form.reason(
                        class_="case-action-field__textarea",
                        rows="5",
                        minlength="10",
                        maxlength="500",
                        required=true,
                        placeholder=(
                            "Example: The assigned department "
                            "lost access to the original secure link."
                        ),
                        aria_describedby=(
                            "reissue-reason-help "
                            "reissue-reason-errors"
                        )
                    )
                }}

                {% if form.reason.errors %}

                    <ul
                        id="reissue-reason-errors"
                        class="case-action-field__errors"
                        aria-live="polite"
                    >
                        {% for error in form.reason.errors %}
                            <li>{{ error }}</li>
                        {% endfor %}
                    </ul>

                {% endif %}

            </div>


            <div class="case-action-form__actions">

                <a
                    href="{{ url_for(
                        'cases.case_detail',
                        case_id=case.id
                    ) }}"
                    class="btn-secondary"
                >
                    Cancel
                </a>

                {{
                    form.submit(
                        class_="btn-primary"
                    )
                }}

            </div>

        </form>

    </section>

</div>

{% endblock %}