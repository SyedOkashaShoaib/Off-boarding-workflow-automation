@case_bp.route(
    "/create",
    methods=["GET", "POST"],
)
@login_required
def create_case():
    """
    Create an offboarding case and send the authorised NOC user
    directly to the initial departmental checklist.

    The initial NOC assignment does not require an email
    notification or task-access token because the creator is already
    authenticated through the operations portal.
    """

    require_case_operations_access()

    form = Case_Form()

    if not form.validate_on_submit():
        return render_template(
            "create_case.html",
            form=form,
        )

    try:
        new_case = OffboardingCase(
            case_number=generate_case_number(),
            employee_name=form.emp_name.data.strip(),
            employee_id=form.emp_id.data,
            designation=form.emp_desig.data.strip(),
            department=form.emp_dep.data.strip(),
            last_working_day=form.last_date.data,
            line_manager=form.line_manager.data.strip(),
            status="CREATED",
            created_by=current_user.email,
        )

        db.session.add(new_case)

        initial_task = create_initial_workflow_task(
            new_case
        )

        # Obtain the generated task ID before committing so the
        # redirect does not depend on accessing an expired ORM object.
        db.session.flush()
        initial_task_id = initial_task.id

        db.session.commit()

    except WorkflowConfigurationError as exc:
        db.session.rollback()

        flash(
            (
                "The offboarding case could not be started because "
                f"the workflow configuration is incomplete: {exc}"
            ),
            "error",
        )

        return render_template(
            "create_case.html",
            form=form,
        )

    except SQLAlchemyError:
        db.session.rollback()

        current_app.logger.exception(
            "Database error while creating an offboarding case."
        )

        flash(
            (
                "A database error occurred while creating the "
                "offboarding case. No case was saved."
            ),
            "error",
        )

        return render_template(
            "create_case.html",
            form=form,
        )

    return redirect(
        url_for(
            "workflow.view_task",
            task_id=initial_task_id,
        )
    )