import hashlib
import secrets

from datetime import datetime, timedelta, timezone
from typing import Optional, Tuple

from flask import current_app, request, session

from app.extension import db
from app.models import (
    AuditLog,
    TaskAccessGrant,
    WorkflowTask,
    utc_now,
)


RAW_TOKEN_BYTES = 32

PENDING_GRANT_SESSION_KEY = (
    "pending_task_access_grant_id"
)

ACTIVE_GRANT_SESSION_KEY = (
    "active_task_access_grant_id"
)

ACTIVE_TASK_SESSION_KEY = (
    "active_task_access_task_id"
)

OPEN_TASK_STATUSES = {
    "PENDING",
    "IN_PROGRESS",
}


def normalize_datetime(
    value: Optional[datetime],
) -> Optional[datetime]:
    """
    Normalize a database datetime into timezone-aware UTC.
    """

    if value is None:
        return None

    if value.tzinfo is None:
        return value.replace(
            tzinfo=timezone.utc
        )

    return value.astimezone(
        timezone.utc
    )


def hash_task_access_token(
    raw_token: str,
) -> str:
    """
    Return the SHA-256 digest stored in the database.
    """

    return hashlib.sha256(
        raw_token.encode("utf-8")
    ).hexdigest()


def revoke_grant(
    grant: TaskAccessGrant,
    *,
    revoked_at: Optional[datetime] = None,
) -> None:
    """
    Revoke one task-access grant.
    """

    if grant.revoked_at is None:
        grant.revoked_at = (
            revoked_at or utc_now()
        )


def revoke_active_task_grants(
    task: WorkflowTask,
) -> None:
    """
    Revoke unconsumed grants previously issued for a task.

    A newly generated assignment link replaces older links.
    """

    current_time = utc_now()

    active_grants = (
        TaskAccessGrant.query
        .filter(
            TaskAccessGrant.workflow_task_id
            == task.id,
            TaskAccessGrant.revoked_at.is_(None),
            TaskAccessGrant.consumed_at.is_(None),
        )
        .all()
    )

    for grant in active_grants:
        grant.revoked_at = current_time

def get_task_access_token_lifetime_hours(
    task: WorkflowTask,
) -> int:
    """
    Return the configured token lifetime for the task type.

    Final-approval grants intentionally expire sooner than ordinary
    departmental checklist grants.
    """

    if task.phase.is_final_approval:
        config_key = (
            "FINAL_APPROVAL_TOKEN_LIFETIME_HOURS"
        )
    else:
        config_key = (
            "TASK_ACCESS_TOKEN_LIFETIME_HOURS"
        )

    return int(
        current_app.config[config_key]
    )

def issue_task_access_grant(
    *,
    task: WorkflowTask,
    recipient_email: str,
) -> Tuple[TaskAccessGrant, str]:
    """
    Generate and persist a new access grant.

    The caller receives the raw token once so it can be inserted
    into the assignment email. Only the token hash is stored.
    """

    cleaned_email = str(
        recipient_email or ""
    ).strip().lower()

    if not cleaned_email:
        raise ValueError(
            "A recipient email address is required."
        )

    revoke_active_task_grants(task)

    raw_token = secrets.token_urlsafe(
        RAW_TOKEN_BYTES
    )

    current_time = utc_now()

    token_lifetime_hours = (
        get_task_access_token_lifetime_hours(
            task
        )
    )

    grant = TaskAccessGrant(
        workflow_task=task,
        token_hash=hash_task_access_token(
            raw_token
        ),
        recipient_email=cleaned_email,
        expires_at=(
            current_time
            + timedelta(
                hours=token_lifetime_hours
            )
        ),
        created_at=current_time,
    )

    db.session.add(grant)

    if task.phase.is_final_approval:
        grant_type = "final-approval"
    else:
        grant_type = "departmental"

    db.session.add(
        AuditLog(
            case=task.case,
            action="TASK_ACCESS_GRANTED",
            performed_by="System",
            details=(
                f"A secure {grant_type} task-access "
                f"grant was issued for task {task.id} "
                f"to '{cleaned_email}'."
            ),
        )
    )

    return grant, raw_token


def grant_is_redeemable(
    grant: Optional[TaskAccessGrant],
) -> bool:
    """
    Return whether a grant may establish a new browser session.

    A grant with an existing activation cannot establish another
    browser session. The already-authorized browser is validated
    separately through its signed Flask session.
    """

    if grant is None:
        return False

    if grant.revoked_at is not None:
        return False

    if grant.consumed_at is not None:
        return False

    if int(grant.access_count or 0) > 0:
        return False

    expires_at = normalize_datetime(
        grant.expires_at
    )

    if (
        expires_at is None
        or expires_at <= utc_now()
    ):
        return False

    task = grant.workflow_task

    if task is None:
        return False

    if task.status not in OPEN_TASK_STATUSES:
        return False

    return True


def find_task_access_grant(
    raw_token: str,
) -> Optional[TaskAccessGrant]:
    """
    Resolve a raw token to its database grant.

    This function performs token lookup only. The caller must
    separately determine whether the current browser already owns
    the grant or whether the grant may establish a new session.
    """

    cleaned_token = str(
        raw_token or ""
    ).strip()

    if (
        not cleaned_token
        or len(cleaned_token) > 512
    ):
        return None

    token_hash = hash_task_access_token(
        cleaned_token
    )

    return (
        TaskAccessGrant.query
        .filter_by(
            token_hash=token_hash
        )
        .first()
    )


def set_pending_task_access(
    grant: TaskAccessGrant,
) -> None:
    """
    Store a validated grant temporarily before user confirmation.
    """

    session[
        PENDING_GRANT_SESSION_KEY
    ] = grant.id


def activate_pending_task_access(
) -> Optional[TaskAccessGrant]:
    """
    Atomically claim a pending grant and bind it to the current
    browser session.

    Only the first confirmation request may change access_count
    from zero to one.
    """

    grant_id = session.get(
        PENDING_GRANT_SESSION_KEY
    )

    if grant_id is None:
        return None

    grant = db.session.get(
        TaskAccessGrant,
        grant_id,
    )

    if not grant_is_redeemable(grant):
        session.pop(
            PENDING_GRANT_SESSION_KEY,
            None,
        )

        return None

    current_time = utc_now()

    # Use a conditional database update rather than only assigning
    # grant.access_count = 1. This prevents two browser sessions
    # that confirmed at nearly the same time from both claiming
    # the grant.
    claimed_row_count = (
        db.session.query(
            TaskAccessGrant
        )
        .filter(
            TaskAccessGrant.id == grant.id,
            TaskAccessGrant.access_count == 0,
            TaskAccessGrant.revoked_at.is_(None),
            TaskAccessGrant.consumed_at.is_(None),
            TaskAccessGrant.expires_at
            > current_time,
        )
        .update(
            {
                TaskAccessGrant.access_count: 1,
                TaskAccessGrant.last_accessed_at: (
                    current_time
                ),
            },
            synchronize_session=False,
        )
    )

    if claimed_row_count != 1:
        session.pop(
            PENDING_GRANT_SESSION_KEY,
            None,
        )

        return None

    # Refresh only the values changed by the conditional update.
    db.session.expire(
        grant,
        [
            "access_count",
            "last_accessed_at",
        ],
    )

    session[
        ACTIVE_GRANT_SESSION_KEY
    ] = grant.id

    session[
        ACTIVE_TASK_SESSION_KEY
    ] = grant.workflow_task_id

    session.pop(
        PENDING_GRANT_SESSION_KEY,
        None,
    )

    db.session.add(
        AuditLog(
            case=grant.workflow_task.case,
            action="TASK_ACCESS_ACTIVATED",
            performed_by=grant.recipient_email,
            details=(
                "A secure workflow task-access "
                "session was activated for task "
                f"{grant.workflow_task_id}."
            ),
        )
    )

    return grant


def get_session_grant_for_task(
    task: WorkflowTask,
    *,
    allow_consumed_read_only: bool = False,
) -> Optional[TaskAccessGrant]:
    """
    Return the grant authorising the current browser session.

    A consumed grant may continue displaying the submitted read-only
    page in the same browser session, but may not submit another POST.
    """

    grant_id = session.get(
        ACTIVE_GRANT_SESSION_KEY
    )

    task_id = session.get(
        ACTIVE_TASK_SESSION_KEY
    )

    if (
        grant_id is None
        or task_id != task.id
    ):
        return None

    grant = db.session.get(
        TaskAccessGrant,
        grant_id,
    )

    if grant is None:
        return None

    if grant.workflow_task_id != task.id:
        return None

    if grant.revoked_at is not None:
        return None

    expires_at = normalize_datetime(
        grant.expires_at
    )

    if (
        expires_at is None
        or expires_at <= utc_now()
    ):
        return None

    if grant.consumed_at is not None:
        if (
            allow_consumed_read_only
            and request.method == "GET"
        ):
            return grant

        return None

    if task.status not in OPEN_TASK_STATUSES:
        return None

    return grant


def consume_task_access_grants(
    task: WorkflowTask,
) -> None:
    """
    Prevent issued links from establishing new sessions after submit.
    """

    current_time = utc_now()

    active_grants = (
        TaskAccessGrant.query
        .filter(
            TaskAccessGrant.workflow_task_id
            == task.id,
            TaskAccessGrant.revoked_at.is_(None),
            TaskAccessGrant.consumed_at.is_(None),
        )
        .all()
    )

    for grant in active_grants:
        grant.consumed_at = current_time

    if active_grants:
        db.session.add(
            AuditLog(
                case=task.case,
                action="TASK_ACCESS_CONSUMED",
                performed_by="System",
                details=(
                    "Task-access grants were consumed after "
                    f"workflow task {task.id} was submitted."
                ),
            )
        )


def get_task_access_actor(
    task: WorkflowTask,
) -> Optional[str]:
    """
    Return the recipient represented by the active task session.
    """

    grant = get_session_grant_for_task(
        task,
        allow_consumed_read_only=True,
    )

    if grant is None:
        return None

    return grant.recipient_email


def clear_task_access_session() -> None:
    """
    Remove task-specific access information from the session.
    """

    session.pop(
        PENDING_GRANT_SESSION_KEY,
        None,
    )

    session.pop(
        ACTIVE_GRANT_SESSION_KEY,
        None,
    )

    session.pop(
        ACTIVE_TASK_SESSION_KEY,
        None,
    )