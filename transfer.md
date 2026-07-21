{% if form.errors %}

    <div
        class="system-message system-message--error"
        role="alert"
    >
        <div>
            <strong>
                The replacement link was not sent.
            </strong>

            <ul>
                {% for field_name, errors in form.errors.items() %}
                    {% for error in errors %}
                        <li>{{ error }}</li>
                    {% endfor %}
                {% endfor %}
            </ul>
        </div>
    </div>

{% endif %}