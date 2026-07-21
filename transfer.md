{% if reissue_task %}

    <a
        href="{{ url_for(
            'cases.reissue_task_access',
            case_id=record.case.id
        ) }}"
        class="
            btn-secondary
            case-reissue-action
        "
    >
        {% if reissue_task.phase.is_final_approval %}
            Reissue Approval Link
        {% else %}
            Reissue
            {{ reissue_task.phase.department.name }}
            Link
        {% endif %}
    </a>

{% endif %}