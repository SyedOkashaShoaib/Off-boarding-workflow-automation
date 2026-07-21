        if access_grant is not None:
            revoke_grant(
                access_grant
            )

        if is_reissue:
            action = "TASK_ACCESS_REISSUE_FAILED"

            details = (
                "The replacement secure access link for "
                f"workflow task {task.id} could not be "
                "delivered to "
                f"'{notification.recipient_email}'. "
                "All previously issued links for this task "
                "remain invalid. Reason: "
                f"{result.error_message or 'No reason returned.'}"
            )

        else:
            action = "TASK_NOTIFICATION_FAILED"

            details = (
                "Task notification failed for "
                f"'{notification.recipient_email}'. "
                "Reason: "
                f"{result.error_message or 'No reason returned.'}"
            )

    db.session.add(
        AuditLog(
            case=task.case,
            action=action,
            performed_by="System",
            details=details,
        )
    )

    return result