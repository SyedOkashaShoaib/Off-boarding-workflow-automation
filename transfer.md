sensitive_output_problems = []

with current_app.test_request_context():
    for case in OffboardingCase.query.all():
        record = get_case_detail_record(
            case.id
        )

        rendered_html = render_template(
            "cases/detail.html",
            record=record,
        ).lower()

        forbidden_terms = [
            "token_hash",
            "task_access_grants",
            "raw_token",
            "/task-access/",
        ]

        detected = [
            term
            for term in forbidden_terms
            if term in rendered_html
        ]

        if detected:
            sensitive_output_problems.append(
                (
                    case.id,
                    case.case_number,
                    detected,
                )
            )

sensitive_output_problems