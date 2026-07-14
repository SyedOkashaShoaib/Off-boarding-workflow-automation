import click
from flask.cli import with_appcontext
from sqlalchemy.exc import (
    IntegrityError,
    SQLAlchemyError,
)

from app.extension import db
from app.models import EmailNotification
from app.services.notification_service import (
    create_overdue_task_notification,
    deliver_overdue_task_notification,
)
from app.services.overdue_service import (
    OverdueConfigurationError,
    build_overdue_deduplication_key,
    find_existing_overdue_notification,
    find_overdue_tasks,
    get_escalation_recipient_email,
    get_overdue_notification_type,
)


@click.command("process-overdue-tasks")
@click.option(
    "--dry-run",
    is_flag=True,
    help=(
        "Show which tasks are overdue without creating "
        "notifications or sending email."
    ),
)
@click.option(
    "--task-id",
    type=int,
    default=None,
    help="Process only one workflow task.",
)
@with_appcontext
def process_overdue_tasks_command(
    dry_run: bool,
    task_id: int | None,
) -> None:
    """
    Find overdue workflow tasks and notify the escalation department.
    """

    try:
        escalation_email = (
            get_escalation_recipient_email()
        )

    except OverdueConfigurationError as exc:
        raise click.ClickException(
            str(exc)
        ) from exc

    overdue_tasks = find_overdue_tasks(
        task_id=task_id
    )

    if not overdue_tasks:
        click.echo("No overdue workflow tasks were found.")
        return

    click.echo(
        f"Found {len(overdue_tasks)} overdue workflow task(s)."
    )

    if dry_run:
        for task in overdue_tasks:
            click.echo(
                (
                    f"[DRY RUN] Task {task.id} | "
                    f"Case {task.case.case_number} | "
                    f"Phase {task.phase.name} | "
                    f"Status {task.status} | "
                    f"Due {task.due_at}"
                )
            )

        click.echo(
            f"Escalation recipient would be: "
            f"{escalation_email}"
        )

        return

    sent_count = 0
    failed_count = 0
    skipped_count = 0

    for task in overdue_tasks:
        deduplication_key = (
            build_overdue_deduplication_key(task)
        )

        notification = (
            find_existing_overdue_notification(
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
                    f"Skipped task {task.id}: today's overdue "
                    "notification was already sent."
                )
            )

            continue

        if notification is None:
            try:
                notification = (
                    create_overdue_task_notification(
                        task=task,
                        recipient_email=escalation_email,
                        notification_type=(
                            get_overdue_notification_type(task)
                        ),
                        deduplication_key=deduplication_key,
                    )
                )

                # Persist the notification before attempting delivery.
                db.session.commit()

            except IntegrityError:
                # Another process may have created the same
                # daily notification after our initial lookup.
                db.session.rollback()

                notification = (
                    EmailNotification.query
                    .filter_by(
                        deduplication_key=deduplication_key
                    )
                    .first()
                )

                if notification is None:
                    failed_count += 1

                    click.echo(
                        (
                            f"Failed task {task.id}: notification "
                            "deduplication conflict could not be "
                            "resolved."
                        ),
                        err=True,
                    )

                    continue

                if notification.status == "SENT":
                    skipped_count += 1
                    continue

            except SQLAlchemyError as exc:
                db.session.rollback()
                failed_count += 1

                click.echo(
                    (
                        f"Failed to queue overdue notification "
                        f"for task {task.id}: {exc}"
                    ),
                    err=True,
                )

                continue

        try:
            result = deliver_overdue_task_notification(
                notification
            )

            db.session.commit()

        except SQLAlchemyError as exc:
            db.session.rollback()
            failed_count += 1

            click.echo(
                (
                    f"Delivery was attempted for task {task.id}, "
                    f"but the result could not be saved: {exc}"
                ),
                err=True,
            )

            continue

        if result.success:
            sent_count += 1

            click.echo(
                (
                    f"Sent overdue escalation for task "
                    f"{task.id}."
                )
            )

        else:
            failed_count += 1

            click.echo(
                (
                    f"Failed overdue escalation for task "
                    f"{task.id}: "
                    f"{result.error_message or 'Unknown error'}"
                ),
                err=True,
            )

    click.echo("")
    click.echo("Overdue processing completed.")
    click.echo(f"Sent: {sent_count}")
    click.echo(f"Failed: {failed_count}")
    click.echo(f"Skipped: {skipped_count}")