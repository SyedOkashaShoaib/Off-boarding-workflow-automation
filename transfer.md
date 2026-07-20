{% if record.case.status == "CLOSED" %}

    <div class="case-detail-empty">

        <h3>Workflow Completed</h3>

        <p>
            This offboarding case is closed and has no active
            departmental assignment.
        </p>

    </div>

{% elif record.current_task %}