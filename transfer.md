@case_bp.route(
    "/<int:case_id>/reissue-access",
    methods=["GET", "POST"],
)
@login_required
def reissue_task_access(case_id):
    """
    Confirm and execute replacement of the secure access link for
    the case's current eligible workflow task.
    """

    require_case_operations_access()

    case = OffboardingCase.query.get_or_404(
        case_id
    )

    try:
        task = get_reissuable_current_task(
            case
        )

    except TaskAccessReissueError as exc:
        flash(
            str(exc),
            "warning",
        )

        return redirect(
            url_for(
                "cases.case_detail",
                case_id=case.id,
            )
        )

    form = ReissueTaskAccessForm()

    if form.validate_on_submit():
        try:
            result = reissue_current_task_access(
                case=case,
                requested_by=current_user.email,
                reason=form.reason.data,
            )

            /*
             * Do not copy this comment syntax into Python.
             */