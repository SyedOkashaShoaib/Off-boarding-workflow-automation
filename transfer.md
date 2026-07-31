from typing import Optional

import click
from flask.cli import with_appcontext
from sqlalchemy.exc import (
    IntegrityError,
    SQLAlchemyError,
)

from app.extension import db
from app.models import EmailNotification
from app.services.notification_service import (
    create_daily_task_reminder_notification,
    deliver_task_assignment_notification,
)
from app.services.reminder_service import (
    build_daily_task_reminder_key,
    find_current_active_tasks,
    find_existing_daily_task_reminder,
)


@click.command(
    "send-daily-task-reminders"
)
@click.option(
    "--dry-run",
    is_flag=True,
    help=(
        "Show which current tasks would receive reminders "
        "without creating notifications, rotating tokens, "
        "or sending email."
    ),
)
@click.option(
    "--task-id",
    type=int,
    default=None,
    help=(
        "Process only one workflow task while retaining all "
        "normal active-task eligibility checks."
    ),
)
@with_appcontext
def send_daily_task_reminders_command(
    dry_run: bool,
    task_id: Optional[int],
) -> None:
    """
    Send one daily reminder to the department responsible for
    each currently active workflow task.

    NOC reminders use authenticated portal links. MIS, Hardware,
    and final Administration reminders receive newly generated
    task-access links that replace previously issued links.
    """

    active_tasks = find_current_active_tasks(
        task_id=task_id
    )

    if not active_tasks:
        click.echo(
            "No current active workflow tasks were found."
        )
        return

    click.echo(
        (
            f"Found {len(active_tasks)} current active "
            "workflow task(s)."
        )
    )

    if dry_run:
        for task in active_tasks:
            click.echo(
                (
                    f"[DRY RUN] Task {task.id} | "
                    f"Case {task.case.case_number} | "
                    f"Phase {task.phase.name} | "
                    f"Department "
                    f"{task.phase.department.name} | "
                    f"Status {task.status} | "
                    f"Recipient "
                    f"{task.assigned_to_email}"
                )
            )

        click.echo("")
        click.echo(
            (
                "Dry run completed. No notifications were "
                "created and no task-access tokens were rotated."
            )
        )
        return

    sent_count = 0
    failed_count = 0
    skipped_count = 0

    for task in active_tasks:
        deduplication_key = (
            build_daily_task_reminder_key(
                task
            )
        )

        notification = (
            find_existing_daily_task_reminder(
                deduplication_key
            )
        )

        if (
            notification is not None
            and notification.status == "SENT"
        ):
            skipped_count += 1

            click.echo(
                (
                    f"Skipped task {task.id}: today's "
                    "reminder was already sent."
                )
            )

            continue

        if notification is None:
            try:
                notification = (
                    create_daily_task_reminder_notification(
                        task=task,
                        deduplication_key=(
                            deduplication_key
                        ),
                    )
                )

                # Store the pending reminder before delivery.
                # This allows failures to be recorded and retried.
                db.session.commit()

            except IntegrityError:
                # Another scheduler process may have created the
                # same task-and-date reminder after our lookup.
                db.session.rollback()

                notification = (
                    EmailNotification.query
                    .filter_by(
                        deduplication_key=(
                            deduplication_key
                        )
                    )
                    .first()
                )

                if notification is None:
                    failed_count += 1

                    click.echo(
                        (
                            f"Failed task {task.id}: the daily "
                            "reminder deduplication conflict "
                            "could not be resolved."
                        ),
                        err=True,
                    )

                    continue

                if notification.status == "SENT":
                    skipped_count += 1

                    click.echo(
                        (
                            f"Skipped task {task.id}: today's "
                            "reminder was sent by another "
                            "process."
                        )
                    )

                    continue

            except (
                SQLAlchemyError,
                ValueError,
            ) as exc:
                db.session.rollback()
                failed_count += 1

                click.echo(
                    (
                        "Failed to queue a daily reminder for "
                        f"task {task.id}: {exc}"
                    ),
                    err=True,
                )

                continue

        try:
            result = (
                deliver_task_assignment_notification(
                    notification
                )
            )

            db.session.commit()

        except SQLAlchemyError as exc:
            db.session.rollback()
            failed_count += 1

            click.echo(
                (
                    f"Delivery was attempted for task "
                    f"{task.id}, but the result could not "
                    f"be saved: {exc}"
                ),
                err=True,
            )

            continue

        if result.success:
            sent_count += 1

            click.echo(
                (
                    "Sent daily reminder for task "
                    f"{task.id} to "
                    f"{notification.recipient_email}."
                )
            )

        else:
            failed_count += 1

            click.echo(
                (
                    "Failed daily reminder for task "
                    f"{task.id}: "
                    f"{result.error_message or 'Unknown error'}"
                ),
                err=True,
            )

    click.echo("")
    click.echo(
        "Daily task-reminder processing completed."
    )
    click.echo(
        f"Sent: {sent_count}"
    )
    click.echo(
        f"Failed: {failed_count}"
    )
    click.echo(
        f"Skipped: {skipped_count}"
    )