{% extends "base.html" %}


{% block title %}
    Cases &middot; Offboarding Workflow System
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
            <li>Operations</li>

            <li aria-current="page">
                Cases
            </li>
        </ol>
    </nav>
{% endblock %}


{% block page_header %}
    <div class="page-header">

        <div>
            <h1>Cases</h1>

            <p>
                Search, filter, and monitor employee offboarding cases.
            </p>
        </div>

        <a
            href="{{ url_for('cases.create_case') }}"
            class="btn-primary"
        >
            Create New Case
        </a>

    </div>
{% endblock %}


{% block content %}

{% set filters = register.filters %}
{% set page = register.page %}
{% set counts = register.counts %}


{% set approval_phase = namespace(slug=None) %}

{% for phase_option in register.phase_options %}
    {% if phase_option.is_final_approval %}
        {% set approval_phase.slug = phase_option.slug %}
    {% endif %}
{% endfor %}


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


{% set attention_labels = {
    "none": "No action required",
    "due_soon": "Due soon",
    "overdue": "Overdue",
    "awaiting_approval": "Awaiting approval",
    "workflow_issue": "Workflow issue"
} %}


<div class="cases-page">

    <!-- =====================================================
         Quick views
         ===================================================== -->
    <div
        class="cases-summary"
        aria-label="Case summary"
    >

        <a
            href="{{ url_for(
                'cases.list_cases',
                status='active',
                due_state='all',
                phase='all',
                per_page=filters.per_page
            ) }}"
            class="
                cases-summary-card

                {% if (
                    filters.case_status == 'active'
                    and filters.due_state == 'all'
                    and not filters.phase_slug
                ) %}
                    cases-summary-card--current
                {% endif %}
            "
        >
            <span class="cases-summary-card__label">
                Active
            </span>

            <strong class="cases-summary-card__value">
                {{ counts.active_cases }}
            </strong>
        </a>


        <a
            href="{{ url_for(
                'cases.list_cases',
                status='active',
                due_state='overdue',
                phase='all',
                per_page=filters.per_page
            ) }}"
            class="
                cases-summary-card

                {% if filters.due_state == 'overdue' %}
                    cases-summary-card--current
                {% endif %}
            "
        >
            <span class="cases-summary-card__label">
                Overdue
            </span>

            <strong class="cases-summary-card__value">
                {{ counts.overdue_cases }}
            </strong>
        </a>


        {% if approval_phase.slug %}

            <a
                href="{{ url_for(
                    'cases.list_cases',
                    status='active',
                    phase=approval_phase.slug,
                    due_state='all',
                    per_page=filters.per_page
                ) }}"
                class="
                    cases-summary-card

                    {% if (
                        filters.case_status == 'active'
                        and filters.phase_slug
                        == approval_phase.slug
                    ) %}
                        cases-summary-card--current
                    {% endif %}
                "
            >
                <span class="cases-summary-card__label">
                    Awaiting Approval
                </span>

                <strong class="cases-summary-card__value">
                    {{ counts.awaiting_approval_cases }}
                </strong>
            </a>

        {% endif %}


        <a
            href="{{ url_for(
                'cases.list_cases',
                status='closed',
                due_state='all',
                phase='all',
                per_page=filters.per_page
            ) }}"
            class="
                cases-summary-card

                {% if filters.case_status == 'closed' %}
                    cases-summary-card--current
                {% endif %}
            "
        >
            <span class="cases-summary-card__label">
                Closed
            </span>

            <strong class="cases-summary-card__value">
                {{ counts.closed_cases }}
            </strong>
        </a>


        <a
            href="{{ url_for(
                'cases.list_cases',
                status='all',
                due_state='all',
                phase='all',
                per_page=filters.per_page
            ) }}"
            class="
                cases-summary-card

                {% if filters.case_status == 'all' %}
                    cases-summary-card--current
                {% endif %}
            "
        >
            <span class="cases-summary-card__label">
                All Cases
            </span>

            <strong class="cases-summary-card__value">
                {{ counts.all_cases }}
            </strong>
        </a>

    </div>


    <!-- =====================================================
         Filters
         ===================================================== -->
    <div class="case-filter-panel">

        <div class="case-filter-panel__heading">
            <h2>Search and Filters</h2>

            <p>
                Filters are applied to the complete case register.
            </p>
        </div>


        <form
            method="get"
            action="{{ url_for('cases.list_cases') }}"
            class="case-filter-form"
        >

            <div class="case-filter-form__search">

                <label for="case-search">
                    Search
                </label>

                <input
                    id="case-search"
                    name="q"
                    type="search"
                    value="{{ filters.search }}"
                    maxlength="100"
                    placeholder="Case number, employee name, or employee ID"
                >

            </div>


            <div>

                <label for="case-status-filter">
                    Case Status
                </label>

                <select
                    id="case-status-filter"
                    name="status"
                >
                    <option
                        value="active"
                        {% if filters.case_status == "active" %}
                            selected
                        {% endif %}
                    >
                        Active
                    </option>

                    <option
                        value="closed"
                        {% if filters.case_status == "closed" %}
                            selected
                        {% endif %}
                    >
                        Closed
                    </option>

                    <option
                        value="all"
                        {% if filters.case_status == "all" %}
                            selected
                        {% endif %}
                    >
                        All
                    </option>
                </select>

            </div>


            <div>

                <label for="phase-filter">
                    Current Phase
                </label>

                <select
                    id="phase-filter"
                    name="phase"
                >
                    <option value="all">
                        All phases
                    </option>

                    {% for phase_option
                       in register.phase_options %}

                        <option
                            value="{{ phase_option.slug }}"

                            {% if (
                                filters.phase_slug
                                == phase_option.slug
                            ) %}
                                selected
                            {% endif %}
                        >
                            {{ phase_option.department_name }}
                            &mdash;
                            {{ phase_option.name }}
                        </option>

                    {% endfor %}
                </select>

            </div>


            <div>

                <label for="due-state-filter">
                    Due State
                </label>

                <select
                    id="due-state-filter"
                    name="due_state"
                >
                    <option
                        value="all"
                        {% if filters.due_state == "all" %}
                            selected
                        {% endif %}
                    >
                        All
                    </option>

                    <option
                        value="on_time"
                        {% if filters.due_state == "on_time" %}
                            selected
                        {% endif %}
                    >
                        On time
                    </option>

                    <option
                        value="due_soon"
                        {% if filters.due_state == "due_soon" %}
                            selected
                        {% endif %}
                    >
                        Due soon
                    </option>

                    <option
                        value="overdue"
                        {% if filters.due_state == "overdue" %}
                            selected
                        {% endif %}
                    >
                        Overdue
                    </option>
                </select>

            </div>


            <div>

                <label for="per-page-filter">
                    Rows
                </label>

                <select
                    id="per-page-filter"
                    name="per_page"
                >
                    {% for page_size in [25, 50, 100] %}

                        <option
                            value="{{ page_size }}"

                            {% if (
                                filters.per_page
                                == page_size
                            ) %}
                                selected
                            {% endif %}
                        >
                            {{ page_size }}
                        </option>

                    {% endfor %}
                </select>

            </div>


            <div class="case-filter-form__actions">

                <button
                    type="submit"
                    class="btn-primary"
                >
                    Apply Filters
                </button>

                <a
                    href="{{ url_for('cases.list_cases') }}"
                    class="btn-secondary"
                >
                    Clear
                </a>

            </div>

        </form>

    </div>


    <!-- =====================================================
         Results
         ===================================================== -->
    <div class="case-register-panel">

        <div class="case-register-panel__heading">

            <div>
                <h2>Case Register</h2>

                {% if page.total > 0 %}

                    {% set first_record =
                        ((page.page - 1) * page.per_page) + 1
                    %}

                    {% set last_record =
                        first_record
                        + (page.items | length)
                        - 1
                    %}

                    <p>
                        Showing
                        {{ first_record }}&ndash;{{ last_record }}
                        of {{ page.total }} matching cases.
                    </p>

                {% else %}

                    <p>
                        No cases match the selected filters.
                    </p>

                {% endif %}
            </div>

        </div>


        {% if page.items %}

            <div
                class="case-table-scroll"
                tabindex="0"
                role="region"
                aria-label="Offboarding case register"
            >

                <table class="case-register-table">

                    <thead>
                        <tr>
                            <th scope="col">Case Number</th>
                            <th scope="col">Employee</th>
                            <th scope="col">Employee Department</th>
                            <th scope="col">Current Phase</th>
                            <th scope="col">Current Task</th>
                            <th scope="col">Due Date</th>
                            <th scope="col">Case Status</th>
                            <th scope="col">Attention</th>

                            <th
                                scope="col"
                                class="
                                    case-register-table__action-column
                                "
                            >
                                Action
                            </th>
                        </tr>
                    </thead>


                    <tbody>

                        {% for item in page.items %}

                            <tr
                                class="case-register-row"
                                data-case-url="{{ url_for(
                                    'cases.case_detail',
                                    case_id=item.case_id
                                ) }}"
                            >

                                <td>
                                    <a
                                        href="{{ url_for(
                                            'cases.case_detail',
                                            case_id=item.case_id
                                        ) }}"
                                        class="
                                            case-number
                                            case-number-link
                                        "
                                        aria-label="
                                            View case
                                            {{ item.case_number }}
                                        "
                                    >
                                        {{ item.case_number }}
                                    </a>

                                    <span class="table-secondary">
                                        Updated
                                        {{
                                            item.updated_at.strftime(
                                                "%d %b %Y"
                                            )
                                        }}
                                    </span>
                                </td>


                                <td>
                                    <strong>
                                        {{ item.employee_name }}
                                    </strong>

                                    <span class="table-secondary">
                                        ID: {{ item.employee_id }}
                                    </span>

                                    <span class="table-secondary">
                                        {{ item.designation }}
                                    </span>
                                </td>


                                <td>
                                    {{ item.employee_department }}
                                </td>


                                <td>
                                    {% if item.current_phase_name %}

                                        <strong>
                                            {{
                                                item.current_department_name
                                                or "Unassigned"
                                            }}
                                        </strong>

                                        <span class="table-secondary">
                                            {{ item.current_phase_name }}
                                        </span>

                                    {% else %}

                                        <span class="table-empty-value">
                                            Not assigned
                                        </span>

                                    {% endif %}
                                </td>


                                <td>
                                    {% if item.current_task_status %}

                                        <span
                                            class="
                                                register-status
                                                register-status--task
                                                register-status--{{
                                                    item.current_task_status
                                                    | lower
                                                }}
                                            "
                                        >
                                            {{
                                                task_status_labels.get(
                                                    item.current_task_status,
                                                    item.current_task_status
                                                    | replace("_", " ")
                                                    | title
                                                )
                                            }}
                                        </span>

                                    {% else %}

                                        <span class="table-empty-value">
                                            No current task
                                        </span>

                                    {% endif %}
                                </td>


                                <td>
                                    {% if item.current_task_due_at %}

                                        {{
                                            item.current_task_due_at.strftime(
                                                "%d %b %Y"
                                            )
                                        }}

                                        <span class="table-secondary">
                                            {{
                                                item.current_task_due_at
                                                .strftime(
                                                    "%I:%M %p"
                                                )
                                            }}
                                        </span>

                                    {% else %}

                                        <span class="table-empty-value">
                                            Not applicable
                                        </span>

                                    {% endif %}
                                </td>


                                <td>
                                    <span
                                        class="
                                            register-status
                                            register-status--case
                                            register-status--{{
                                                item.case_status | lower
                                            }}
                                        "
                                    >
                                        {{
                                            case_status_labels.get(
                                                item.case_status,
                                                item.case_status
                                                | replace("_", " ")
                                                | title
                                            )
                                        }}
                                    </span>
                                </td>


                                <td>
                                    <span
                                        class="
                                            attention-indicator
                                            attention-indicator--{{
                                                item.attention_code
                                            }}
                                        "
                                    >
                                        {{
                                            attention_labels.get(
                                                item.attention_code,
                                                "Review required"
                                            )
                                        }}
                                    </span>
                                </td>


                                <td
                                    class="
                                        case-register-table__action-cell
                                    "
                                >
                                    <a
                                        href="{{ url_for(
                                            'cases.case_detail',
                                            case_id=item.case_id
                                        ) }}"
                                        class="
                                            btn-secondary
                                            case-register-view-link
                                        "
                                        aria-label="
                                            View details for
                                            {{ item.case_number }}
                                        "
                                    >
                                        View details
                                    </a>
                                </td>

                            </tr>

                        {% endfor %}

                    </tbody>

                </table>

            </div>


            {% if page.pages > 1 %}

                <nav
                    class="case-pagination"
                    aria-label="Case register pages"
                >

                    <div class="case-pagination__summary">
                        Page {{ page.page }} of {{ page.pages }}
                    </div>


                    <div class="case-pagination__controls">

                        {% if page.has_previous %}

                            <a
                                href="{{ url_for(
                                    'cases.list_cases',
                                    q=filters.search,
                                    status=filters.case_status,
                                    phase=filters.phase_slug or 'all',
                                    due_state=filters.due_state,
                                    per_page=filters.per_page,
                                    page=page.previous_page
                                ) }}"
                                class="btn-secondary"
                                rel="prev"
                            >
                                Previous
                            </a>

                        {% else %}

                            <span
                                class="btn-secondary"
                                aria-disabled="true"
                            >
                                Previous
                            </span>

                        {% endif %}


                        {% if page.has_next %}

                            <a
                                href="{{ url_for(
                                    'cases.list_cases',
                                    q=filters.search,
                                    status=filters.case_status,
                                    phase=filters.phase_slug or 'all',
                                    due_state=filters.due_state,
                                    per_page=filters.per_page,
                                    page=page.next_page
                                ) }}"
                                class="btn-secondary"
                                rel="next"
                            >
                                Next
                            </a>

                        {% else %}

                            <span
                                class="btn-secondary"
                                aria-disabled="true"
                            >
                                Next
                            </span>

                        {% endif %}

                    </div>

                </nav>

            {% endif %}


        {% else %}

            <div class="case-register-empty">

                <h3>No Matching Cases</h3>

                <p>
                    Adjust the search criteria or clear the selected
                    filters to view additional cases.
                </p>

                <a
                    href="{{ url_for('cases.list_cases') }}"
                    class="btn-secondary"
                >
                    Clear Filters
                </a>

            </div>

        {% endif %}

    </div>

</div>

{% endblock %}


{% block scripts %}
    <script
        src="{{ url_for(
            'static',
            filename='js/cases.js'
        ) }}"
        defer
    ></script>
{% endblock %}