(.venv) PS C:\Users\intern\Desktop\intern_summer_26\offboarding_workflow> git show --name-status --format="COMMIT %h %ad %s" --date=short 6008177
COMMIT 6008177 2026-07-22 add accountable checklist response controls

M       app/static/css/pages/task.css
M       app/static/js/task_checklist.js
M       app/templates/workflow/task_detail.html
(.venv) PS C:\Users\intern\Desktop\intern_summer_26\offboarding_workflow> 
(.venv) PS C:\Users\intern\Desktop\intern_summer_26\offboarding_workflow> git diff --unified=200 6008177^ 6008177 -- app/templates/workflow/task_detail.html
diff --git a/app/templates/workflow/task_detail.html b/app/templates/workflow/task_detail.html
index 698b5dc..c43969a 100644
--- a/app/templates/workflow/task_detail.html
+++ b/app/templates/workflow/task_detail.html
@@ -1,763 +1,926 @@
 {% extends "layouts/task_base.html" %}


 {% block title %}
     {{ task.case.case_number }} · Department Task
 {% endblock %}


 {% block head %}
-    <link
-        rel="stylesheet"
-        href="{{ url_for(
-            'static',
-            filename='css/pages/task.css'
-        ) }}"
-    >
+    {{ super() }}
 {% endblock %}


 {% block breadcrumbs %}
-    <nav
-        class="breadcrumbs"
-        aria-label="Breadcrumb"
-    >
-        <ol class="breadcrumbs__list">
-            <li>Operations</li>
-            <li aria-current="page">
-                Department Task
-            </li>
-        </ol>
-    </nav>
+    <ol class="breadcrumbs">
+        <li class="breadcrumbs__item">
+            Operations
+        </li>
+
+        <li
+            class="breadcrumbs__item breadcrumbs__item--current"
+            aria-current="page"
+        >
+            Department Task
+        </li>
+    </ol>
 {% endblock %}


 {% block page_header %}
-    <div class="task-page-heading">
-        <div>
-            <h1>Department Offboarding Task</h1>
+    <h1>Department Offboarding Task</h1>

-            <p>
-                Complete the assigned clearance checklist for
-                {{ task.phase.department.name }}.
-            </p>
-        </div>
-    </div>
+    <p>
+        Complete the assigned clearance checklist for
+        {{ task.phase.department.name }}.
+    </p>
 {% endblock %}


 {% block content %}
-
-{% set submitted = task.status == "SUBMITTED" %}
-
-{% set status_labels = {
-    "PENDING": "Pending",
-    "IN_PROGRESS": "In Progress",
-    "SUBMITTED": "Submitted",
-    "APPROVED": "Approved"
-} %}
-
-{% set status_label = status_labels.get(
-    task.status,
-    task.status | replace("_", " ") | title
-) %}
-
-
-<div class="task-page">
-
-    <!-- =====================================================
-         Task identity and deadline
-         ===================================================== -->
-    <div class="task-hero">
-
-        <div class="task-hero__identity">
-
-            <span class="task-hero__eyebrow">
+    {% set submitted = (
+        task.submitted_at is not none
+        or task.status in [
+            "SUBMITTED",
+            "COMPLETED",
+            "APPROVED"
+        ]
+    ) %}
+
+    {% set status_labels = {
+        "PENDING": "Pending",
+        "IN_PROGRESS": "In Progress",
+        "SUBMITTED": "Submitted",
+        "COMPLETED": "Completed",
+        "APPROVED": "Approved"
+    } %}
+
+    {% set status_label = status_labels.get(
+        task.status,
+        task.status | replace("_", " ") | title
+    ) %}
+
+
+    <section class="task-summary-card">
+        <div class="task-summary-card__case">
+            <span class="task-summary-card__label">
                 Case Number
             </span>

-            <strong class="task-hero__case-number">
+            <strong class="task-summary-card__case-number">
                 {{ task.case.case_number }}
             </strong>
+        </div>

-            <h2 class="task-hero__phase">
-                {{ task.phase.name }}
-            </h2>
-
-            <p class="task-hero__department">
-                Responsible department:
-                <strong>
-                    {{ task.phase.department.name }}
-                </strong>
-            </p>
+        <div class="task-summary-card__main">
+            <div>
+                <p class="task-summary-card__eyebrow">
+                    Workflow phase
+                </p>

-        </div>
+                <h2 class="task-summary-card__title">
+                    {{ task.phase.name }}
+                </h2>

+                <p class="task-summary-card__department">
+                    Responsible department:
+                    <strong>
+                        {{ task.phase.department.name }}
+                    </strong>
+                </p>
+            </div>

-        <dl class="task-hero__status">
+            <span
+                class="
+                    status-badge
+                    status-badge--{{
+                        task.status
+                        | lower
+                        | replace('_', '-')
+                    }}
+                "
+            >
+                {{ status_label }}
+            </span>
+        </div>

+        <dl class="task-summary-card__metadata">
             <div>
                 <dt>Status</dt>
-                <dd>
-                    <span
-                        class="
-                            task-status
-                            task-status--{{ task.status | lower }}
-                        "
-                    >
-                        {{ status_label }}
-                    </span>
-                </dd>
+                <dd>{{ status_label }}</dd>
             </div>

             <div>
                 <dt>Due Date</dt>
                 <dd>
-                    {{ task.due_at.strftime(
-                        "%d %B %Y, %I:%M %p"
-                    ) }}
+                    {% if task.due_at %}
+                        {{ task.due_at.strftime(
+                            "%d %B %Y, %I:%M %p"
+                        ) }}
+                    {% else %}
+                        Not assigned
+                    {% endif %}
                 </dd>
             </div>
-
         </dl>
-
-    </div>
+    </section>


-    <!-- =====================================================
-         Employee information
-         ===================================================== -->
-    <div class="task-panel">
-
-        <div class="task-panel__heading">
+    <section class="information-card">
+        <header class="information-card__header">
             <h2>Employee Information</h2>
-        </div>
-
-        <dl class="task-information-grid">
+        </header>

-            <div>
+        <dl class="information-grid">
+            <div class="information-grid__item">
                 <dt>Employee Name</dt>
                 <dd>{{ task.case.employee_name }}</dd>
             </div>

-            <div>
+            <div class="information-grid__item">
                 <dt>Employee ID</dt>
                 <dd>{{ task.case.employee_id }}</dd>
             </div>

-            <div>
+            <div class="information-grid__item">
                 <dt>Designation</dt>
                 <dd>{{ task.case.designation }}</dd>
             </div>

-            <div>
+            <div class="information-grid__item">
                 <dt>Employee Department</dt>
                 <dd>{{ task.case.department }}</dd>
             </div>

-            <div>
+            <div class="information-grid__item">
                 <dt>Line Manager</dt>
                 <dd>{{ task.case.line_manager }}</dd>
             </div>

-            <div>
+            <div class="information-grid__item">
                 <dt>Last Working Day</dt>
                 <dd>
-                    {{ task.case.last_working_day.strftime(
-                        "%d %B %Y"
-                    ) }}
+                    {% if task.case.last_working_day %}
+                        {{ task.case.last_working_day.strftime(
+                            "%d %B %Y"
+                        ) }}
+                    {% else %}
+                        Not recorded
+                    {% endif %}
                 </dd>
             </div>
-
         </dl>
+    </section>

-    </div>
-
-
-    <!-- =====================================================
-         Workflow progress
-         ===================================================== -->
-    <!-- <div class="task-panel">
-
-        <div class="task-panel__heading">
-            <h2>Workflow Progress</h2>
-            <p>
-                Clearance proceeds through each department in order.
-            </p>
-        </div>
-
-        <ol
-            class="workflow-progress"
-            aria-label="Offboarding workflow progress"
-        >
-
-            {% for progress_item in workflow_progress %}
-
-                <li
-                    class="
-                        workflow-progress__item
-                        workflow-progress__item--{{ progress_item.state }}
-                    "
-
-                    {% if progress_item.state == "current" %}
-                        aria-current="step"
-                    {% endif %}
-                >
-
-                    <span
-                        class="workflow-progress__marker"
-                        aria-hidden="true"
-                    >
-                        {% if progress_item.state == "completed" %}
-                            ✓
-                        {% else %}
-                            {{ loop.index }}
-                        {% endif %}
-                    </span>
-
-                    <span class="workflow-progress__content">
-
-                        <strong>
-                            {{ progress_item.phase.department.name }}
-                        </strong>
-
-                        <span>
-                            {% if progress_item.state == "completed" %}
-                                Completed
-                            {% elif progress_item.state == "current" %}
-                                Current phase
-                            {% else %}
-                                Upcoming
-                            {% endif %}
-                        </span>
-
-                    </span>
-
-                </li>
-
-            {% endfor %}

-        </ol>
-
-    </div> -->
-
-
-    <!-- =====================================================
-         Submitted confirmation
-         ===================================================== -->
     {% if submitted %}
-
-    <div
-        class="task-submitted-panel"
-        role="status"
-    >
-
-        <div
-            class="task-submitted-panel__icon"
-            aria-hidden="true"
+        <section
+            class="task-alert task-alert--success"
+            role="status"
         >
-            ✓
-        </div>
+            <div class="task-alert__icon" aria-hidden="true">
+                ✓
+            </div>

-        <div>
-            <h2>Checklist Submitted</h2>
+            <div>
+                <h2>Checklist Submitted</h2>
 
-            {% if task.submitted_at %}
-                <p>
-                    Your department’s clearance responses were
-                    recorded successfully on
-                    <strong>
+                {% if task.submitted_at %}
+                    <p>
+                        Your department’s clearance responses were
+                        recorded successfully on
                         {{ task.submitted_at.strftime(
                             "%d %B %Y, %I:%M %p"
-                        ) }}
-                    </strong>.
-                </p>
-            {% else %}
+                        ) }}.
+                    </p>
+                {% else %}
+                    <p>
+                        Your department’s clearance responses were
+                        recorded successfully.
+                    </p>
+                {% endif %}
+
                 <p>
-                    Your department’s clearance responses were
-                    recorded successfully.
+                    This task is now read-only.
                 </p>
-            {% endif %}
-
-            <p>
-                This task is now read-only.
-            </p>
-        </div>
-
-    </div>
-
-{% endif %}
+            </div>
+        </section>
+    {% endif %}

-    <!-- =====================================================
-         Validation summary
-         ===================================================== -->
     {% if validation_errors %}
-
-        <div
-            id="checklist-error-summary"
-            class="checklist-error-summary"
+        <section
+            class="validation-summary"
             role="alert"
-            tabindex="-1"
+            aria-labelledby="validation-summary-title"
         >
-
-            <h2>
+            <h2 id="validation-summary-title">
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
-                   in validation_errors.items() %}
-
+                    in validation_errors.items() %}
                     <li>
-                        <a href="#checklist-item-{{ item_id }}">
-                            {{ error_message }}
-                        </a>
+                        {{ error_message }}
                     </li>
-
                 {% endfor %}
             </ul>
+        </section>
+    {% endif %}

-        </div>

+    {% if form.csrf_token.errors %}
+        <section
+            class="validation-summary"
+            role="alert"
+        >
+            <h2>Form security error</h2>
+
+            <ul>
+                {% for error in form.csrf_token.errors %}
+                    <li>{{ error }}</li>
+                {% endfor %}
+            </ul>
+        </section>
     {% endif %}

-    <!-- =====================================================
-         Checklist
-         ===================================================== -->
     {% if checklist_sections %}
-
         {% if not submitted %}
-
             <form
                 method="post"
-                action="{{ url_for(
-                    'workflow.view_task',
-                    task_id=task.id
-                ) }}"
                 class="checklist-form"
                 data-checklist-form
             >
-
                 {{ form.hidden_tag() }}
-
         {% endif %}


-        {% set item_counter = namespace(value=0) %}
-
-        {% for section_name, checklist_items
-           in checklist_sections.items() %}
-
-            <div class="checklist-section">
+        {% if not submitted and not department_employees %}
+            <div
+                class="task-alert task-alert--error"
+                role="alert"
+            >
+                <div>
+                    <strong>
+                        No responsible employees are available.
+                    </strong>

-                <div class="checklist-section__heading">
+                    <p>
+                        This checklist cannot be submitted until at
+                        least one active employee is configured for
+                        {{ task.phase.department.name }}.
+                    </p>
+                </div>
+            </div>
+        {% endif %}

-                    <h2>{{ section_name }}</h2>

-                    <span>
-                        {{ checklist_items | length }}
-                        {% if checklist_items | length == 1 %}
-                            item
-                        {% else %}
-                            items
-                        {% endif %}
-                    </span>
+        <div class="checklist-sections">
+            {% set item_counter = namespace(value=0) %}

-                </div>
+            {% for section_name, checklist_items
+                in checklist_sections.items() %}

+                <section
+                    class="checklist-section"
+                    aria-labelledby="
+                        checklist-section-{{ loop.index }}
+                    "
+                >
+                    <header class="checklist-section__header">
+                        <div>
+                            <p class="checklist-section__eyebrow">
+                                Checklist section
+                            </p>
+
+                            <h2
+                                class="checklist-section__title"
+                                id="checklist-section-{{ loop.index }}"
+                            >
+                                {{ section_name }}
+                            </h2>
+                        </div>
+
+                        <span class="checklist-section__count">
+                            {{ checklist_items | length }}
+
+                            {% if checklist_items | length == 1 %}
+                                item
+                            {% else %}
+                                items
+                            {% endif %}
+                        </span>
+                    </header>

-                <div class="checklist-section__items">

-                    {% for checklist_item in checklist_items %}
+                    <div class="checklist-section__items">
+                        {% for checklist_item
+                            in checklist_items %}

-                        {% set item_counter.value =
-                            item_counter.value + 1
-                        %}
+                            {% set item_counter.value = (
+                                item_counter.value + 1
+                            ) %}

-                        {% set saved_value =
-                            submitted_values.get(
+                            {% set saved_value = submitted_values.get(
                                 checklist_item.id,
                                 {}
-                            )
-                        %}
+                            ) %}

-                        {% set selected_response =
-                            saved_value.get(
+                            {% set selected_response = saved_value.get(
                                 "response_status",
                                 ""
-                            )
-                        %}
+                            ) %}

-                        {% set saved_reason =
-                            saved_value.get(
+                            {% set saved_reason = saved_value.get(
                                 "reason",
                                 ""
-                            )
-                        %}
-
-                        {% set item_error =
-                            validation_errors.get(
-                                checklist_item.id
-                            )
-                        %}
+                            ) %}

+                            {% set selected_employee_id = (
+                                saved_value.get(
+                                    "responsible_employee_id",
+                                    ""
+                                )
+                            ) %}

-                        <article
-                            id="checklist-item-{{ checklist_item.id }}"
-                            class="
-                                checklist-item
-
-                                {% if item_error %}
-                                    checklist-item--error
-                                {% endif %}
-                            "
-                            data-checklist-item
-                            tabindex="{% if item_error %}-1{% else %}0{% endif %}"
-                        >
-
-                            <header class="checklist-item__header">
-
-                                <span class="checklist-item__number">
-                                    {{ item_counter.value }}
-                                </span>
-
-                                <div>
-                                    <h3>
-                                        {{ checklist_item.item_text }}
-                                    </h3>
-
-                                    {% if (
-                                        checklist_item.is_required
-                                        and not submitted
-                                    ) %}
-                                        <span class="required-text">
-                                            Response required
-                                        </span>
+                            {% set item_error = validation_errors.get(
+                                checklist_item.id
+                            ) %}
+
+                            {% set recorded_response = (
+                                task.responses
+                                | selectattr(
+                                    "checklist_item_id",
+                                    "equalto",
+                                    checklist_item.id
+                                )
+                                | first
+                            ) %}
+
+                            {% set help_id = (
+                                "checklist-help-"
+                                ~ checklist_item.id
+                            ) %}
+
+                            {% set error_id = (
+                                "checklist-error-"
+                                ~ checklist_item.id
+                            ) %}
+
+
+                            <article
+                                class="
+                                    checklist-item
+                                    {% if item_error %}
+                                        checklist-item--invalid
                                     {% endif %}
-                                </div>
-
-                            </header>
-
-
-                            {% if submitted %}
-
-                                <div class="recorded-response">
-
-                                    <span class="recorded-response__label">
-                                        Recorded Response
-                                    </span>
+                                "
+                                data-checklist-item
+                                data-item-id="{{ checklist_item.id }}"
+                            >
+                                <div class="checklist-item__heading">
+                                    <div
+                                        class="checklist-item__number"
+                                        aria-hidden="true"
+                                    >
+                                        {{ item_counter.value }}
+                                    </div>

-                                    <strong>
-                                        {% if selected_response == "YES" %}
-                                            Yes
-                                        {% elif selected_response
-                                            == "NOT_APPLICABLE" %}
-                                            Not Applicable
-                                        {% else %}
-                                            Not recorded
-                                        {% endif %}
-                                    </strong>
-
-                                    {% if (
-                                        selected_response
-                                        == "NOT_APPLICABLE"
-                                    ) %}
-                                        <div class="recorded-reason">
-                                            <span>
-                                                Reason
+                                    <div>
+                                        <h3
+                                            class="checklist-item__title"
+                                        >
+                                            {{ checklist_item.item_text }}
+                                        </h3>
+
+                                        {% if not submitted %}
+                                            <span
+                                                class="
+                                                    checklist-item__required
+                                                "
+                                            >
+                                                Response required
                                             </span>
-
-                                            <p>
-                                                {{
-                                                    saved_reason
-                                                    or
-                                                    "No reason recorded."
-                                                }}
-                                            </p>
-                                        </div>
-                                    {% endif %}
-
+                                        {% endif %}
+                                    </div>
                                 </div>

-                            {% else %}

-                                <fieldset
-                                    class="response-fieldset"
-
-                                    {% if item_error %}
-                                        aria-invalid="true"
-                                        aria-describedby="
-                                            item-error-{{ checklist_item.id }}
+                                {% if submitted %}
+                                    <div
+                                        class="
+                                            checklist-recorded-response
                                         "
-                                    {% endif %}
-                                >
-
-                                    <legend>Response</legend>
-
-                                    <div class="response-options">
-
-                                        <label class="response-option">
-
-                                            <input
-                                                type="radio"
-                                                name="response_{{ checklist_item.id }}"
-                                                value="YES"
+                                    >
+                                        <div
+                                            class="
+                                                checklist-recorded-response__item
+                                            "
+                                        >
+                                            <span
+                                                class="
+                                                    checklist-recorded-response__label
+                                                "
+                                            >
+                                                Recorded Response
+                                            </span>

-                                                {% if selected_response == "YES" %}
-                                                    checked
+                                            <strong>
+                                                {% if (
+                                                    selected_response
+                                                    == "YES"
+                                                ) %}
+                                                    Yes
+                                                {% elif (
+                                                    selected_response
+                                                    == "NO"
+                                                ) %}
+                                                    No
+                                                {% elif (
+                                                    selected_response
+                                                    == "NOT_APPLICABLE"
+                                                ) %}
+                                                    Not applicable
+                                                {% else %}
+                                                    Not recorded
                                                 {% endif %}
+                                            </strong>
+                                        </div>

-                                                required
-                                            >

-                                            <span>
-                                                <strong>Yes</strong>
-                                                <small>
-                                                    The required action
-                                                    has been completed.
-                                                </small>
+                                        <div
+                                            class="
+                                                checklist-recorded-response__item
+                                            "
+                                        >
+                                            <span
+                                                class="
+                                                    checklist-recorded-response__label
+                                                "
+                                            >
+                                                Responsible Employee
                                             </span>

-                                        </label>
+                                            <strong>
+                                                {% if (
+                                                    recorded_response
+                                                    and
+                                                    recorded_response
+                                                    .responsible_employee
+                                                ) %}
+                                                    {{
+                                                        recorded_response
+                                                        .responsible_employee
+                                                        .full_name
+                                                    }}
+
+                                                    {% if (
+                                                        recorded_response
+                                                        .responsible_employee
+                                                        .employee_code
+                                                    ) %}
+                                                        —
+                                                        {{
+                                                            recorded_response
+                                                            .responsible_employee
+                                                            .employee_code
+                                                        }}
+                                                    {% endif %}
+                                                {% else %}
+                                                    Not recorded
+                                                {% endif %}
+                                            </strong>
+                                        </div>


-                                        <label class="response-option">
+                                        {% if selected_response in [
+                                            "NO",
+                                            "NOT_APPLICABLE"
+                                        ] %}
+                                            <div
+                                                class="
+                                                    checklist-recorded-response__item
+                                                    checklist-recorded-response__item--full
+                                                "
+                                            >
+                                                <span
+                                                    class="
+                                                        checklist-recorded-response__label
+                                                    "
+                                                >
+                                                    Reason
+                                                </span>
+
+                                                <p>
+                                                    {{
+                                                        saved_reason
+                                                        or
+                                                        "No reason recorded."
+                                                    }}
+                                                </p>
+                                            </div>
+                                        {% endif %}
+                                    </div>

-                                            <input
-                                                type="radio"
-                                                name="response_{{ checklist_item.id }}"
-                                                value="NOT_APPLICABLE"
+                                {% else %}
+                                    <div
+                                        class="checklist-item__fields"
+                                    >
+                                        <fieldset
+                                            class="response-fieldset"
+                                            aria-describedby="{{ help_id }}{% if item_error %} {{ error_id }}{% endif %}"
+                                        >
+                                            <legend class="form-label">
+                                                Response
+
+                                                <span
+                                                    class="required-marker"
+                                                    aria-hidden="true"
+                                                >
+                                                    *
+                                                </span>
+                                            </legend>
+
+                                            <p
+                                                class="form-help"
+                                                id="{{ help_id }}"
+                                            >
+                                                Select one response for
+                                                this checklist item.
+                                            </p>

-                                                {% if selected_response == "NOT_APPLICABLE" %}
-                                                    checked
-                                                {% endif %}

+                                            <div
+                                                class="response-options"
+                                                data-response-options
+                                            >
+                                                <label
+                                                    class="
+                                                        response-option
+                                                        {% if (
+                                                            selected_response
+                                                            == "YES"
+                                                        ) %}
+                                                            response-option--selected
+                                                        {% endif %}
+                                                    "
+                                                >
+                                                    <input
+                                                        type="radio"
+                                                        name="response_{{ checklist_item.id }}"
+                                                        value="YES"
+                                                        data-response-option
+                                                        required
+                                                        {% if selected_response == "YES" %}
+                                                            checked
+                                                        {% endif %}
+                                                    >
+
+                                                    <span
+                                                        class="
+                                                            response-option__content
+                                                        "
+                                                    >
+                                                        <strong>
+                                                            Yes
+                                                        </strong>
+
+                                                        <small>
+                                                            The required
+                                                            action was
+                                                            completed.
+                                                        </small>
+                                                    </span>
+                                                </label>
+
+
+                                                <label
+                                                    class="
+                                                        response-option
+                                                        {% if (
+                                                            selected_response
+                                                            == "NO"
+                                                        ) %}
+                                                            response-option--selected
+                                                        {% endif %}
+                                                    "
+                                                >
+                                                    <input
+                                                        type="radio"
+                                                        name="response_{{ checklist_item.id }}"
+                                                        value="NO"
+                                                        data-response-option
+                                                        required
+                                                        {% if selected_response == "NO" %}
+                                                            checked
+                                                        {% endif %}
+                                                    >
+
+                                                    <span
+                                                        class="
+                                                            response-option__content
+                                                        "
+                                                    >
+                                                        <strong>
+                                                            No
+                                                        </strong>
+
+                                                        <small>
+                                                            The required
+                                                            action was not
+                                                            completed.
+                                                        </small>
+                                                    </span>
+                                                </label>
+
+
+                                                <label
+                                                    class="
+                                                        response-option
+                                                        {% if (
+                                                            selected_response
+                                                            == "NOT_APPLICABLE"
+                                                        ) %}
+                                                            response-option--selected
+                                                        {% endif %}
+                                                    "
+                                                >
+                                                    <input
+                                                        type="radio"
+                                                        name="response_{{ checklist_item.id }}"
+                                                        value="NOT_APPLICABLE"
+                                                        data-response-option
+                                                        required
+                                                        {% if selected_response == "NOT_APPLICABLE" %}
+                                                            checked
+                                                        {% endif %}
+                                                    >
+
+                                                    <span
+                                                        class="
+                                                            response-option__content
+                                                        "
+                                                    >
+                                                        <strong>
+                                                            Not applicable
+                                                        </strong>
+
+                                                        <small>
+                                                            This action does
+                                                            not apply.
+                                                        </small>
+                                                    </span>
+                                                </label>
+                                            </div>
+                                        </fieldset>
+
+
+                                        <div class="form-group">
+                                            <label
+                                                class="form-label"
+                                                for="responsible-employee-{{ checklist_item.id }}"
+                                            >
+                                                Responsible employee
+
+                                                <span
+                                                    class="required-marker"
+                                                    aria-hidden="true"
+                                                >
+                                                    *
+                                                </span>
+                                            </label>
+
+                                            <select
+                                                class="form-control"
+                                                id="responsible-employee-{{ checklist_item.id }}"
+                                                name="responsible_employee_{{ checklist_item.id }}"
+                                                data-responsible-employee
                                                 required
+                                                {% if not department_employees %}
+                                                    disabled
+                                                {% endif %}
+                                                {% if item_error %}
+                                                    aria-invalid="true"
+                                                    aria-describedby="{{ error_id }}"
+                                                {% endif %}
                                             >
+                                                <option value="">
+                                                    Select an employee
+                                                </option>
+
+                                                {% for employee
+                                                    in department_employees %}
+                                                    <option
+                                                        value="{{ employee.id }}"
+                                                        {% if employee.id|string == selected_employee_id|string %}
+                                                            selected
+                                                        {% endif %}
+                                                    >
+                                                        {{ employee.full_name }}
+
+                                                        {% if employee.employee_code %}
+                                                            —
+                                                            {{ employee.employee_code }}
+                                                        {% endif %}
+                                                    </option>
+                                                {% endfor %}
+                                            </select>
+
+                                            <p class="form-help">
+                                                Select the employee
+                                                responsible for this
+                                                individual checklist item.
+                                            </p>
+                                        </div>

-                                            <span>
-                                                <strong>
-                                                    Not Applicable
-                                                </strong>
-
-                                                <small>
-                                                    This control or asset
-                                                    was not assigned.
-                                                </small>
-                                            </span>

-                                        </label>
+                                        <div
+                                            class="form-group reason-field"
+                                            data-reason-container
+                                            {% if selected_response not in [
+                                                "NO",
+                                                "NOT_APPLICABLE"
+                                            ] %}
+                                                hidden
+                                            {% endif %}
+                                        >
+                                            <label
+                                                class="form-label"
+                                                for="response-reason-{{ checklist_item.id }}"
+                                                data-reason-label
+                                            >
+                                                {% if selected_response == "NO" %}
+                                                    Reason for No
+                                                {% elif selected_response == "NOT_APPLICABLE" %}
+                                                    Reason for Not applicable
+                                                {% else %}
+                                                    Reason or explanation
+                                                {% endif %}
+                                            </label>
+
+                                            <textarea
+                                                class="
+                                                    form-control
+                                                    form-control--textarea
+                                                "
+                                                id="response-reason-{{ checklist_item.id }}"
+                                                name="reason_{{ checklist_item.id }}"
+                                                rows="3"
+                                                maxlength="2000"
+                                                data-reason-input
+                                                {% if selected_response in [
+                                                    "NO",
+                                                    "NOT_APPLICABLE"
+                                                ] %}
+                                                    required
+                                                    aria-required="true"
+                                                {% else %}
+                                                    aria-required="false"
+                                                {% endif %}
+                                                {% if item_error %}
+                                                    aria-invalid="true"
+                                                    aria-describedby="{{ error_id }}"
+                                                {% endif %}
+                                            >{{ saved_reason }}</textarea>

+                                            <p
+                                                class="form-help"
+                                                data-reason-hint
+                                            >
+                                                {% if selected_response == "NO" %}
+                                                    Explain why the action
+                                                    was not completed.
+                                                {% elif selected_response == "NOT_APPLICABLE" %}
+                                                    Explain why this action
+                                                    does not apply.
+                                                {% else %}
+                                                    Required when the
+                                                    response is No or Not
+                                                    applicable.
+                                                {% endif %}
+                                            </p>
+                                        </div>
                                     </div>

-                                </fieldset>
-
-
-                                <div
-                                    class="not-applicable-reason"
-                                    data-reason-container
-                                >
-
-                                    <label
-                                        for="reason_{{ checklist_item.id }}"
-                                    >
-                                        Reason for Not Applicable
-                                    </label>
-
-                                    <p class="field-help">
-                                        Required only when
-                                        “Not Applicable” is selected.
-                                    </p>
-
-                                    <textarea
-                                        id="reason_{{ checklist_item.id }}"
-                                        name="reason_{{ checklist_item.id }}"
-                                        rows="3"
-                                        maxlength="2000"
-                                        data-reason-input
-                                    >{{ saved_reason }}</textarea>
-
-                                </div>
-
-
-                                {% if item_error %}
-
-                                    <p
-                                        id="item-error-{{ checklist_item.id }}"
-                                        class="checklist-item__error"
-                                    >
-                                        {{ item_error }}
-                                    </p>

+                                    {% if item_error %}
+                                        <div
+                                            class="
+                                                checklist-item__error
+                                            "
+                                            id="{{ error_id }}"
+                                            role="alert"
+                                        >
+                                            {{ item_error }}
+                                        </div>
+                                    {% endif %}
                                 {% endif %}
-
-                            {% endif %}
-
-                        </article>
-
-                    {% endfor %}
-
-                </div>
-
-            </div>
-
-        {% endfor %}
+                            </article>
+                        {% endfor %}
+                    </div>
+                </section>
+            {% endfor %}
+        </div>


         {% if not submitted %}
-
-
-                <div class="checklist-actions">
+            <section class="checklist-submit-panel">
+                <div>
+                    <h2>Submit Checklist</h2>

                     <p>
                         Review every response carefully. Submitting
                         this checklist advances the case to the next
                         workflow phase, and the responses cannot
                         currently be edited afterward.
                     </p>
+                </div>

+                {% if department_employees %}
                     {{ form.submit(
                         class_="btn-primary checklist-submit-button"
                     ) }}
-
-                </div>
+                {% else %}
+                    {{ form.submit(
+                        class_="btn-primary checklist-submit-button",
+                        disabled=True
+                    ) }}
+                {% endif %}
+            </section>

             </form>
-
-
-            <dialog
-                id="checklist-submit-dialog"
-                class="confirmation-dialog"
-                aria-labelledby="submit-dialog-title"
-                aria-describedby="submit-dialog-description"
-            >
-
-                <div class="confirmation-dialog__titlebar">
-                    <h2 id="submit-dialog-title">
-                        Submit Checklist?
-                    </h2>
-                </div>
-
-                <div class="confirmation-dialog__content">
-
-                    <p id="submit-dialog-description">
-                        Your responses will be recorded and the
-                        offboarding case will advance to the next
-                        department.
-                    </p>
-
-                    <p>
-                        The checklist cannot currently be edited
-                        after submission.
-                    </p>
-
-                </div>
-
-                <div class="confirmation-dialog__actions">
-
-                    <button
-                        type="button"
-                        class="btn-secondary"
-                        data-dialog-cancel
-                    >
-                        Cancel
-                    </button>
-
-                    <button
-                        type="button"
-                        class="btn-primary"
-                        data-dialog-confirm
-                    >
-                        Submit Checklist
-                    </button>
-
-                </div>
-
-            </dialog>
-
         {% endif %}

-
     {% else %}
-
-        <div class="task-empty-state">
-
+        <section class="empty-state">
             <h2>Checklist Unavailable</h2>

             <p>
                 No active checklist items are configured for this
                 workflow phase. Contact the workflow administrator
                 before continuing.
             </p>
-
-        </div>
-
+        </section>
     {% endif %}


-    <!-- =====================================================
-         Assignment metadata
-         ===================================================== -->
-    <details class="task-technical-details">
+    <section class="assignment-details">
+        <h2>Assignment Details</h2>

-        <summary>
-            Assignment Details
-        </summary>
-
-        <dl>
-
-            <div>
+        <dl class="information-grid">
+            <div class="information-grid__item">
                 <dt>Assigned Email</dt>
                 <dd>{{ task.assigned_to_email }}</dd>
             </div>

-            <div>
+            <div class="information-grid__item">
                 <dt>Assigned At</dt>
                 <dd>
-                    {{ task.assigned_at.strftime(
-                        "%d %B %Y, %I:%M %p"
-                    ) }}
+                    {% if task.assigned_at %}
+                        {{ task.assigned_at.strftime(
+                            "%d %B %Y, %I:%M %p"
+                        ) }}
+                    {% else %}
+                        Not recorded
+                    {% endif %}
                 </dd>
             </div>

-            <div>
+            <div class="information-grid__item">
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
-
         </dl>
-
-    </details>
-
-</div>
-
+    </section>
 {% endblock %}


 {% block scripts %}
+    {{ super() }}
+
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
\ No newline at end of file
(.venv) PS C:\Users\intern\Desktop\intern_summer_26\offboarding_workflow> git ls-files | Select-String -Pattern 'task_detail | task_checklist | checklist | task_base'
(.venv) PS C:\Users\intern\Desktop\intern_summer_26\offboarding_workflow> 
