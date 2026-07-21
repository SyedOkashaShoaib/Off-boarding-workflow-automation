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

            db.session.commit()

        except TaskAccessReissueError as exc:
            db.session.rollback()

            flash(
                str(exc),
                "error",
            )

            return redirect(
                url_for(
                    "cases.case_detail",
                    case_id=case.id,
                )
            )

        except SQLAlchemyError:
            db.session.rollback()

            current_app.logger.exception(
                (
                    "Database error while reissuing secure "
                    "task access for case %s."
                ),
                case.id,
            )

            flash(
                (
                    "The replacement-link request could not "
                    "be saved. No reliable reissue result "
                    "was recorded."
                ),
                "error",
            )

            return redirect(
                url_for(
                    "cases.case_detail",
                    case_id=case.id,
                )
            )

        if result.delivery_result.success:
            flash(
                (
                    "A replacement secure link for "
                    f"{result.task.phase.department.name} "
                    "was sent to "
                    f"{result.notification.recipient_email}. "
                    "All previous links and browser sessions "
                    "for this task are now invalid."
                ),
                "success",
            )

        else:
            flash(
                (
                    "All previous links for the current task "
                    "were invalidated, but the replacement "
                    "notification could not be delivered. "
                    "Check the recipient or email configuration "
                    "and reissue the link again."
                ),
                "warning",
            )

        return redirect(
            url_for(
                "cases.case_detail",
                case_id=case.id,
            )
        )

    return render_template(
        "cases/reissue_access.html",
        case=case,
        task=task,
        form=form,
    )