def create_task_access_reissue_notification(
    *,
    task: WorkflowTask,
    requested_by: str,
    reason: str,
) -> EmailNotification:
    """
    Create a pending notification for a replacement secure link.

    This function does not deliver the notification and does not
    commit the database transaction.
    """

    if task.phase.is_final_approval:
        subject = (
            "Replacement Final Approval Link — "
            f"{task.case.case_number}"
        )
    else:
        subject = (
            "Replacement Offboarding Access Link — "
            f"{task.case.case_number}"
        )

    notification = EmailNotification(
        case=task.case,
        workflow_task=task,
        notification_type=(
            TASK_ACCESS_REISSUE_NOTIFICATION_TYPE
        ),
        recipient_email=task.assigned_to_email,
        subject=subject,
        status="PENDING",
    )

    db.session.add(notification)

    db.session.add(
        AuditLog(
            case=task.case,
            action="TASK_ACCESS_REISSUE_REQUESTED",
            performed_by=requested_by,
            details=(
                "A replacement secure access link was "
                f"requested for task {task.id}. "
                f"Department: {task.phase.department.name}. "
                f"Recipient: '{task.assigned_to_email}'. "
                f"Reason: {reason}"
            ),
        )
    )

    return notification