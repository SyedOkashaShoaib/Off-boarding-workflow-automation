from typing import Optional
from urllib.parse import (
    urljoin,
    urlsplit,
    urlunsplit,
)

from flask import (
    Blueprint,
    abort,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from flask_login import (
    current_user,
    login_required,
    login_user,
    logout_user,
)
from sqlalchemy.exc import SQLAlchemyError

from app.extension import db
from app.forms.auth_forms import (
    LoginForm,
    LogoutForm,
)
from app.models import (
    User,
    utc_now,
)


auth_bp = Blueprint(
    "auth",
    __name__,
    url_prefix="/auth",
)


def get_safe_local_redirect(
    target: Optional[str],
) -> Optional[str]:
    """
    Return a same-host relative redirect target.

    Flask-Login supplies the originally requested page through the
    `next` parameter. It must not be trusted without validation.
    """

    if not target:
        return None

    application_url = urlsplit(
        request.host_url
    )

    resolved_url = urlsplit(
        urljoin(
            request.host_url,
            str(target),
        )
    )

    if resolved_url.scheme not in {
        "http",
        "https",
    }:
        return None

    if resolved_url.netloc != application_url.netloc:
        return None

    if not resolved_url.path.startswith("/"):
        return None

    # Return only the local path, query string, and fragment.
    return urlunsplit(
        (
            "",
            "",
            resolved_url.path,
            resolved_url.query,
            resolved_url.fragment,
        )
    )


@auth_bp.route(
    "/login",
    methods=["GET", "POST"],
)
def login():
    """
    Authenticate an authorised portal user.
    """

    requested_next = request.args.get(
        "next",
        "",
    )

    if current_user.is_authenticated:
        redirect_target = get_safe_local_redirect(
            requested_next
        )

        return redirect(
            redirect_target
            or url_for("cases.list_cases")
        )

    form = LoginForm()

    if request.method == "GET":
        form.next_url.data = requested_next

    if form.validate_on_submit():
        normalized_email = User.normalize_email(
            form.email.data
        )

        user = (
            User.query
            .filter_by(
                email=normalized_email
            )
            .first()
        )

        credentials_are_valid = (
            user is not None
            and user.is_active
            and user.check_password(
                form.password.data
            )
        )

        if not credentials_are_valid:
            # Use one generic error so the page does not disclose
            # whether the email address exists.
            form.password.errors.append(
                "Email or password is incorrect."
            )

            return render_template(
                "auth/login.html",
                form=form,
            )

        # Clear any existing anonymous-session data before placing
        # the authenticated user ID into the new session.
        session.clear()

        login_succeeded = login_user(
            user,
            remember=False,
            fresh=True,
        )

        if not login_succeeded:
            form.password.errors.append(
                "This account is not permitted to sign in."
            )

            return render_template(
                "auth/login.html",
                form=form,
            )

        # Last-login recording is useful operational metadata, but
        # failure to update it should not invalidate valid credentials.
        try:
            user.last_login_at = utc_now()
            db.session.commit()

        except SQLAlchemyError:
            db.session.rollback()

            current_app.logger.exception(
                (
                    "Portal login succeeded for user %s, "
                    "but last_login_at could not be updated."
                ),
                user.id,
            )

        redirect_target = get_safe_local_redirect(
            form.next_url.data
        )

        return redirect(
            redirect_target
            or url_for("cases.list_cases")
        )

    return render_template(
        "auth/login.html",
        form=form,
    )


@auth_bp.post("/logout")
@login_required
def logout():
    """
    End the current authenticated portal session.
    """

    form = LogoutForm()

    if not form.validate_on_submit():
        abort(400)

    logout_user()
    session.clear()

    flash(
        "You have been signed out.",
        "info",
    )

    return redirect(
        url_for("auth.login")
    )