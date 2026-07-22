def build_saved_response_values(
    task: WorkflowTask,
) -> dict:
    """
    Convert saved ChecklistResponse records into values displayed
    by the task template.
    """

    return {
        response.checklist_item_id: {
            "response_status": (
                response.response_status
            ),
            "reason": (
                response.response_reason or ""
            ),
            "responsible_employee_id": (
                response.responsible_employee_id
            ),
        }
        for response in task.responses
    }