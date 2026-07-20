from app.models import from app.services.case_detail_service import (
    get_case_detail_record,
)

service_failures = []

for case in OffboardingCase.query.order_by(
    OffboardingCase.id.asc()
).all():
    try:
        record = get_case_detail_record(
            case.id
        )

        if record is None:
            service_failures.append(
                (
                    case.id,
                    case.case_number,
                    "Service returned None",
                )
            )

    except Exception as exc:
        service_failures.append(
            (
                case.id,
                case.case_number,
                type(exc).__name__,
                str(exc),
            )
        )

service_failures

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