from flask import (
    Blueprint,
    redirect,
    url_for,
)
from flask_login import current_user


main_bp = Blueprint(
    "main",
    __name__,
)


@main_bp.get("/")
def home():
    """
    Send users to the appropriate application entry point.
    """

    if current_user.is_authenticated:
        return redirect(
            url_for("cases.list_cases")
        )

    return redirect(
        url_for("auth.login")
    )