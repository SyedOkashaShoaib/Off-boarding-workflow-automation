@case_bp.get("/<int:case_id>")
@login_required
def case_detail(case_id):
    """
    Display the complete read-only operational record for one
    offboarding case.

    Access is restricted to NOC portal operators and technical
    system administrators.
    """

    if not current_user.has_role(
        ROLE_NOC_OPERATOR,
        ROLE_SYSTEM_ADMIN,
    ):
        abort(403)

    record = get_case_detail_record(
        case_id
    )

    if record is None:
        abort(404)

    return render_template(
        "cases/detail.html",
        record=record,
    )