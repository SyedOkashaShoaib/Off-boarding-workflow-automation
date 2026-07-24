{% else %}
    <div class="checklist-item__fields">

        <fieldset
            class="response-fieldset"
            aria-describedby="
                checklist-guidance
                {{ help_id }}
                {% if item_error %}
                    {{ error_id }}
                {% endif %}
            "
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
                class="visually-hidden"
                id="{{ help_id }}"
            >
                Choose one response for this checklist item.
            </p>

            <div
                class="response-options"
                data-response-options
            >
                <label
                    class="
                        response-option
                        response-option--yes
                        {% if selected_response == 'YES' %}
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

                    <span class="response-option__content">
                        <span
                            class="response-option__indicator"
                            aria-hidden="true"
                        ></span>

                        <strong>Yes</strong>
                    </span>
                </label>

                <label
                    class="
                        response-option
                        response-option--no
                        {% if selected_response == 'NO' %}
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

                    <span class="response-option__content">
                        <span
                            class="response-option__indicator"
                            aria-hidden="true"
                        ></span>

                        <strong>No</strong>
                    </span>
                </label>

                <label
                    class="
                        response-option
                        response-option--not-applicable
                        {% if (
                            selected_response
                            == 'NOT_APPLICABLE'
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
                        {% if (
                            selected_response
                            == "NOT_APPLICABLE"
                        ) %}
                            checked
                        {% endif %}
                    >

                    <span class="response-option__content">
                        <span
                            class="response-option__indicator"
                            aria-hidden="true"
                        ></span>

                        <strong>Not applicable</strong>
                    </span>
                </label>
            </div>
        </fieldset>

        <div
            class="
                form-group
                responsible-employee-field
            "
        >
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
                aria-describedby="
                    checklist-guidance
                    {% if item_error %}
                        {{ error_id }}
                    {% endif %}
                "
                {% if not department_employees %}
                    disabled
                {% endif %}
                {% if item_error %}
                    aria-invalid="true"
                {% endif %}
            >
                <option value="">
                    Select responsible employee
                </option>

                {% for employee in department_employees %}
                    <option
                        value="{{ employee.id }}"
                        {% if (
                            employee.id|string
                            == selected_employee_id|string
                        ) %}
                            selected
                        {% endif %}
                    >
                        {{ employee.full_name }}

                        {% if employee.employee_code %}
                            — {{ employee.employee_code }}
                        {% endif %}
                    </option>
                {% endfor %}
            </select>
        </div>

        <div
            class="form-group reason-field"
            id="reason-container-{{ checklist_item.id }}"
            data-reason-container
            aria-live="polite"
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
                    Reason action was not completed
                {% elif (
                    selected_response
                    == "NOT_APPLICABLE"
                ) %}
                    Reason action does not apply
                {% else %}
                    Reason
                {% endif %}

                <span
                    class="required-marker"
                    aria-hidden="true"
                >
                    *
                </span>
            </label>

            <textarea
                class="
                    form-control
                    form-control--textarea
                "
                id="response-reason-{{ checklist_item.id }}"
                name="reason_{{ checklist_item.id }}"
                rows="2"
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
                    Explain why the action was not completed.
                {% elif (
                    selected_response
                    == "NOT_APPLICABLE"
                ) %}
                    Explain why this action does not apply.
                {% else %}
                    Required for No or Not applicable.
                {% endif %}
            </p>
        </div>
    </div>