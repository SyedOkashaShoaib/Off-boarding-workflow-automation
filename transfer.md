from app.models import OffboardingCase

[
    {
        "id": case.id,
        "case_number": case.case_number,
        "employee": case.employee_name,
    }
    for case in (
        OffboardingCase.query
        .order_by(OffboardingCase.id.desc())
        .limit(10)
        .all()
    )
]