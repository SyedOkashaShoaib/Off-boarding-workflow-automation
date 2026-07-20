    current_task = next(
        (
            task
            for task in tasks
            if task.phase_id
            == case.current_phase_id
        ),
        None,
    )

    audit_logs = sorted(
        case.audit_logs,
        key=lambda audit_log: (
            audit_log.created_at,
            audit_log.id,
        ),
        reverse=True,
    )

    final_task = next(
        (
            task
            for task in tasks
            if task.phase.is_final_approval
        ),
        None,
    )

    final_approval_log = next(
        (
            audit_log
            for audit_log in audit_logs
            if audit_log.action
            == "FINAL_APPROVAL_GRANTED"
        ),
        None,
    )

    return CaseDetailRecord(
        case=case,
        tasks=tasks,
        current_task=current_task,
        final_task=final_task,
        final_approval_log=final_approval_log,
        audit_logs=audit_logs,
    )