from app.models import OffboardingCase

case_inventory = [
    {
        "id": case.id,
        "case_number": case.case_number,
        "status": case.status,
        "current_phase_id": case.current_phase_id,
        "task_count": len(case.tasks),
        "employee": case.employee_name,
    }
    for case in (
        OffboardingCase.query
        .order_by(OffboardingCase.id.asc())
        .all()
    )
]

case_inventory