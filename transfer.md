{% block page_header %}

    <div class="page-header">

        <div>
            <h1>{{ record.case.case_number }}</h1>

            <p>
                {{ record.case.employee_name }}
                &middot; Employee offboarding case
            </p>
        </div>


        <div class="case-detail-actions">

            <button
                type="button"
                class="btn-primary"
                data-print-case
                data-case-number="{{ record.case.case_number }}"
            >
                Print Case
            </button>


            <a
                href="{{ url_for('cases.list_cases') }}"
                class="btn-secondary"
            >
                Back to Cases
            </a>

        </div>

    </div>

{% endblock %}