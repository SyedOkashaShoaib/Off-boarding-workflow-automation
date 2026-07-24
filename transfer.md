<section
    class="task-record-panel"
    aria-labelledby="task-record-panel-title"
>
    <header class="task-record-panel__header">
        <h2 id="task-record-panel-title">
            Offboarding Task Information
        </h2>
    </header>

    <dl class="task-record-grid">
        <div class="task-record-grid__item">
            <dt>Case Number</dt>

            <dd>
                {{ task.case.case_number }}
            </dd>
        </div>

        <div class="task-record-grid__item">
            <dt>Case Status</dt>

            <dd>
                {{
                    (task.case.status or "Not recorded")
                    | replace("_", " ")
                    | title
                }}
            </dd>
        </div>

        <div class="task-record-grid__item">
            <dt>Task Status</dt>

            <dd>
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
            </dd>
        </div>

        <div class="task-record-grid__item">
            <dt>Due Date</dt>

            <dd>
                {% if task.due_at %}
                    {{
                        task.due_at.strftime(
                            "%d %B %Y, %I:%M %p"
                        )
                    }}
                {% else %}
                    Not assigned
                {% endif %}
            </dd>
        </div>

        <div class="task-record-grid__item">
            <dt>Workflow Phase</dt>

            <dd>
                {{ task.phase.name }}
            </dd>
        </div>

        <div class="task-record-grid__item">
            <dt>Responsible Department</dt>

            <dd>
                {{ task.phase.department.name }}
            </dd>
        </div>

        <div class="task-record-grid__item">
            <dt>Employee Name</dt>

            <dd>
                {{ task.case.employee_name }}
            </dd>
        </div>

        <div class="task-record-grid__item">
            <dt>Employee ID</dt>

            <dd>
                {{ task.case.employee_id }}
            </dd>
        </div>

        <div class="task-record-grid__item">
            <dt>Designation</dt>

            <dd>
                {{ task.case.designation }}
            </dd>
        </div>

        <div class="task-record-grid__item">
            <dt>Employee Department</dt>

            <dd>
                {{ task.case.department }}
            </dd>
        </div>

        <div class="task-record-grid__item">
            <dt>Line Manager</dt>

            <dd>
                {{ task.case.line_manager or "Not recorded" }}
            </dd>
        </div>

        <div class="task-record-grid__item">
            <dt>Last Working Day</dt>

            <dd>
                {% if task.case.last_working_day %}
                    {{
                        task.case.last_working_day.strftime(
                            "%d %B %Y"
                        )
                    }}
                {% else %}
                    Not recorded
                {% endif %}
            </dd>
        </div>
    </dl>
</section>