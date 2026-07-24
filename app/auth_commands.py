import click
from flask.cli import with_appcontext
from sqlalchemy.exc import SQLAlchemyError

from app.extension import db
from app.models import (
    PORTAL_ROLES,
    ROLE_NOC_OPERATOR,
    User,
)


@click.command(
    "create-portal-user"
)
@click.option(
    "--email",
    prompt="Email address",
    help="Corporate email address used for portal login.",
)
@click.option(
    "--full-name",
    prompt="Full name",
    help="User's display name.",
)
@click.option(
    "--role",
    type=click.Choice(
        PORTAL_ROLES,
        case_sensitive=False,
    ),
    default=ROLE_NOC_OPERATOR,
    show_default=True,
    help="Portal authorization role.",
)
@click.option(
    "--password",
    prompt=True,
    hide_input=True,
    confirmation_prompt=True,
    help="Initial portal password.",
)
@with_appcontext
def create_portal_user_command(
    email: str,
    full_name: str,
    role: str,
    password: str,
) -> None:
    """
    Create an authenticated portal account.

    There is deliberately no public user-registration page.
    Portal accounts are provisioned through an administrative
    process until corporate identity integration is implemented.
    """

    normalized_email = User.normalize_email(
        email
    )

    normalized_full_name = str(
        full_name or ""
    ).strip()

    normalized_role = str(
        role or ""
    ).strip().upper()

    if not normalized_email:
        raise click.ClickException(
            "Email address is required."
        )

    if not normalized_full_name:
        raise click.ClickException(
            "Full name is required."
        )

    if len(password) < 3: #change this later on.... :)
        raise click.ClickException(
            "Password must contain at least 3 characters."
        )

    existing_user = (
        User.query
        .filter_by(
            email=normalized_email
        )
        .first()
    )

    if existing_user is not None:
        raise click.ClickException(
            "A portal user with that email already exists."
        )

    user = User(
        email=normalized_email,
        full_name=normalized_full_name,
        role=normalized_role,
        active=True,
    )

    user.set_password(password)

    try:
        db.session.add(user)
        db.session.commit()

    except (SQLAlchemyError, ValueError) as exc:
        db.session.rollback()

        raise click.ClickException(
            "The portal user could not be created."
        ) from exc

    click.echo(
        (
            "Portal user created successfully: "
            f"{user.email} [{user.role}]"
        )
    )