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

                        <span
                            class="table-empty-value"
                            aria-label="No reason required"
                            title="No reason required"
                        >
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

                        <strong
                            class="
                                checklist-responsible-employee__name
                            "
                        >
                            {{ responsible_employee.full_name }}
                        </strong>

                        {% if responsible_employee.employee_code %}
                            <span
                                class="
                                    checklist-responsible-employee__code
                                "
                            >
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