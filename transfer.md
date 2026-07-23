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