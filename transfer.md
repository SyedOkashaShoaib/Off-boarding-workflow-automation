from flask import (
    current_app,
    render_template,
)

render_failures = []

with current_app.test_request_context():
    for case in OffboardingCase.query.order_by(
        OffboardingCase.id.asc()
    ).all():
        try:
            record = get_case_detail_record(
                case.id
            )

            rendered_html = render_template(
                "cases/detail.html",
                record=record,
            )

            if not rendered_html.strip():
                render_failures.append(
                    (
                        case.id,
                        case.case_number,
                        "Empty rendered output",
                    )
                )

        except Exception as exc:
            render_failures.append(
                (
                    case.id,
                    case.case_number,
                    type(exc).__name__,
                    str(exc),
                )
            )

render_failures