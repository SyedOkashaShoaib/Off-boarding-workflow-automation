def deliver_task_assignment_notification(
    notification: EmailNotification,
) -> EmailResult:
    """
    Deliver either an initial assignment notification or a
    replacement secure-link notification.

    NOC tasks use portal authentication. MIS, Hardware, and
    Administration tasks receive task-specific secure links.

    This function updates the active SQLAlchemy session but does
    not commit it.
    """

    task = notification.workflow_task

    access_grant = None

    notification.attempted_at = utc_now()
    notification.provider_message_id = None
    notification.error_message = None
    notification.sent_at = None

    is_final_approval = bool(
        task.phase.is_final_approval
    )

    is_reissue = (
        notification.notification_type
        == TASK_ACCESS_REISSUE_NOTIFICATION_TYPE
    )

    if is_reissue and is_final_approval:
        message_heading = (
            "Replacement Final Approval Link"
        )

        message_intro = (
            "A replacement secure link has been issued for "
            "the final Administration approval task. Any "
            "previous link and previously authorized browser "
            "session for this task are no longer valid."
        )

        link_label = "Open Final Approval"

    elif is_reissue:
        message_heading = (
            "Replacement Offboarding Access Link"
        )

        message_intro = (
            "A replacement secure link has been issued for "
            "this offboarding task. Any previous link and "
            "previously authorized browser session for this "
            "task are no longer valid."
        )

        link_label = "Open Assigned Task"

    elif is_final_approval:
        message_heading = (
            "Final Offboarding Approval Required"
        )

        message_intro = (
            "The departmental clearance phases have been "
            "completed. Final Administration review and "
            "approval are now required."
        )

        link_label = "Open Final Approval"

    else:
        message_heading = (
            "Offboarding Action Required"
        )

        message_intro = (
            "A new employee offboarding task has been "
            "assigned."
        )

        link_label = "Open Assigned Task"

    try:
        requires_portal_login = (
            task_requires_portal_login(task)
        )

        if requires_portal_login:
            task_url = build_portal_task_url(
                task
            )

            security_notice = (
                "Sign in through the authorised "
                "offboarding operations portal to "
                "open this assignment."
            )

        else:
            (
                access_grant,
                raw_token,
            ) = issue_task_access_grant(
                task=task,
                recipient_email=(
                    notification.recipient_email
                ),
            )

            task_url = build_task_access_url(
                raw_token
            )

            if is_final_approval:
                security_notice = (
                    "This secure link authorizes access "
                    "only to this final-approval task. "
                    "Do not forward or share it."
                )

            else:
                security_notice = (
                    "This secure link is intended only "
                    "for the assigned department. "
                    "Do not forward or share it."
                )

        due_at_text = format_datetime(
            task.due_at
        )

        text_body = f"""
{message_heading}

{message_intro}

Case Number: {task.case.case_number}
Employee: {task.case.employee_name}
Employee ID: {task.case.employee_id}
Phase: {task.phase.name}
Assigned Department: {task.phase.department.name}
Due At: {due_at_text}

{link_label}: {task_url}

Security notice: {security_notice}
        """.strip()

        html_body = f"""
<!doctype html>
<html lang="en">
<body>
    <h1>{escape(message_heading)}</h1>

    <p>{escape(message_intro)}</p>

    <table>
        <tbody>
            <tr>
                <th align="left">Case Number</th>
                <td>{escape(task.case.case_number)}</td>
            </tr>

            <tr>
                <th align="left">Employee</th>
                <td>{escape(task.case.employee_name)}</td>
            </tr>

            <tr>
                <th align="left">Employee ID</th>
                <td>{escape(task.case.employee_id)}</td>
            </tr>

            <tr>
                <th align="left">Phase</th>
                <td>{escape(task.phase.name)}</td>
            </tr>

            <tr>
                <th align="left">Assigned Department</th>
                <td>
                    {escape(task.phase.department.name)}
                </td>
            </tr>

            <tr>
                <th align="left">Due At</th>
                <td>{escape(due_at_text)}</td>
            </tr>
        </tbody>
    </table>

    <p>
        <a href="{escape(task_url)}">
            {escape(link_label)}
        </a>
    </p>

    <p>
        <strong>Security notice:</strong>
        {escape(security_notice)}
    </p>
</body>
</html>
        """.strip()

        result = send_notification_email(
            notification=notification,
            html_body=html_body,
            text_body=text_body,
        )

    except Exception as exc:
        current_app.logger.exception(
            (
                "Could not prepare task assignment "
                "notification %s."
            ),
            notification.id,
        )

        result = EmailResult(
            success=False,
            error_message=str(exc),
        )

    notification.provider_message_id = (
        result.provider_message_id
    )

    notification.error_message = (
        result.error_message
    )

    if result.success:
        notification.status = "SENT"
        notification.sent_at = utc_now()
        notification.error_message = None

        if is_reissue:
            action = "TASK_ACCESS_REISSUE_SENT"

            details = (
                "A replacement secure access link for "
                f"workflow task {task.id} was sent to "
                f"'{notification.recipient_email}'."
            )

        else:
            action = "TASK_NOTIFICATION_SENT"

            details = (
                "Task notification sent to "
                f"'{notification.recipient_email}'."
            )

    else:
        notification.status = "FAILED"
        notification.sent_at = None

        /*
         * This comment belongs in JavaScript, not Python.
         */