def render_task_detail(
    *,
    task: WorkflowTask,
    form: WorkflowChecklistForm,
    checklist_sections: dict,
    department_employees: list,
    submitted_values: dict,
    validation_errors: dict,
):
    """
    Render the departmental task page with complete checklist
    context.

    Every render path must use this helper so submitted selections
    survive validation failures.
    """

    return render_template(
        "workflow/task_detail.html",
        task=task,
        form=form,
        checklist_sections=checklist_sections,
        department_employees=(
            department_employees
        ),
        submitted_values=submitted_values,
        validation_errors=validation_errors,
    )