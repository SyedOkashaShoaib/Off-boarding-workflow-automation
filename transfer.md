def create_daily_task_reminder_notification(
    *,
    task: WorkflowTask,
    deduplication_key: str,
) -> EmailNotification:
    """
    Create one pending daily reminder for the task that is
    currently active for an offboarding case.

    Delivery is performed separately. For token-authorized
    departments, delivery generates a fresh access token and
    revokes previously active grants.
    """

    recipient_email = str(
        task.assigned_to_email or ""
    ).strip().lower()

    if not recipient_email:
        raise ValueError(
            (
                "The active workflow task does not have "
                "a recipient email address."
            )
        )

    normalized_key = str(
        deduplication_key or ""
    ).strip()

    if not normalized_key:
        raise ValueError(
            (
                "A deduplication key is required for a "
                "daily task reminder."
            )
        )

    if task.phase.is_final_approval:
        subject = (
            "Daily Reminder — Final Offboarding "
            "Approval Required — "
            f"{task.case.case_number}"
        )
    else:
        subject = (
            "Daily Reminder — Offboarding Action "
            "Required — "
            f"{task.case.case_number}"
        )

    notification = EmailNotification(
        case=task.case,
        workflow_task=task,
        notification_type=(
            DAILY_TASK_REMINDER_NOTIFICATION_TYPE
        ),
        deduplication_key=normalized_key,
        recipient_email=recipient_email,
        subject=subject,
        status="PENDING",
    )

    db.session.add(
        notification
    )

    db.session.add(
        AuditLog(
            case=task.case,
            action="DAILY_REMINDER_QUEUED",
            performed_by="System",
            details=(
                "A daily reminder was queued for "
                f"workflow task {task.id}. "
                f"Department: "
                f"{task.phase.department.name}. "
                f"Recipient: "
                f"'{recipient_email}'."
            ),
        )
    )

    return notification