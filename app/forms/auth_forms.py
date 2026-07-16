from flask_wtf import FlaskForm
from wtforms import (
    HiddenField,
    PasswordField,
    StringField,
    SubmitField,
)
from wtforms.validators import (
    DataRequired,
    Email,
    Length,
)


class LoginForm(FlaskForm):
    """
    Portal login form.

    The hidden next_url field preserves the protected page the user
    originally requested. The route must validate it before redirecting.
    """

    email = StringField(
        "Email Address",
        validators=[
            DataRequired(
                message="Email address is required."
            ),
            Email(
                message="Enter a valid email address."
            ),
            Length(
                max=254,
                message=(
                    "Email address cannot exceed "
                    "254 characters."
                ),
            ),
        ],
    )

    password = PasswordField(
        "Password",
        validators=[
            DataRequired(
                message="Password is required."
            ),
            Length(
                max=512,
                message="Password is too long.",
            ),
        ],
    )

    next_url = HiddenField()

    submit = SubmitField("Sign In")


class LogoutForm(FlaskForm):
    """
    CSRF-protected logout request.
    """

    submit = SubmitField("Sign Out")