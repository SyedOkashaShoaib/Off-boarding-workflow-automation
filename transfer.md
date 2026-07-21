<section
    class="case-print-header"
    aria-label="Printed case record heading"
>

    <div class="case-print-header__identity">

        <div>
            <strong class="case-print-header__company">
                Barrett Hodgson
            </strong>

            <span class="case-print-header__system">
                Offboarding Workflow System
            </span>
        </div>


        <div class="case-print-header__document">
            Employee Offboarding Case Record
        </div>

    </div>


    <dl class="case-print-header__metadata">

        <div>
            <dt>Case Number</dt>

            <dd>
                {{ record.case.case_number }}
            </dd>
        </div>


        <div>
            <dt>Employee</dt>

            <dd>
                {{ record.case.employee_name }}
            </dd>
        </div>


        <div>
            <dt>Employee ID</dt>

            <dd>
                {{ record.case.employee_id }}
            </dd>
        </div>


        <div>
            <dt>Record Printed</dt>

            <dd data-print-generated-at>
                Prepared for printing
            </dd>
        </div>

    </dl>

</section>


<div class="case-detail-page">