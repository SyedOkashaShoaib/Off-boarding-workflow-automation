@case_bp.get("/<int:case_id>")
@login_required
def case_detail(case_id):
    """
    Display the complete read-only operational record for one
    offboarding case.
    """

    require_case_operations_access()

    record = get_case_detail_record(
        case_id
    )

    if record is None:
        abort(404)

    reissue_task = None

    try:
        reissue_task = (
            get_reissuable_current_task(
                record.case
            )
        )

    except TaskAccessReissueError:
        # An ineligible case remains viewable without a button.
        pass

    return render_template(
        "cases/detail.html",
        record=record,
        reissue_task=reissue_task,
    )