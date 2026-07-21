from flask_wtf import FlaskForm

from wtforms import (
    SubmitField,
    TextAreaField,
)

from wtforms.validators import (
    DataRequired,
    Length,
)


class ReissueTaskAccessForm(FlaskForm):
    """
    Confirmation form for replacing the secure link assigned to
    the current departmental workflow task.
    """

    reason = TextAreaField(
        "Reason for reissuing the secure link",
        validators=[
            DataRequired(
                message=(
                    "Explain why a replacement secure link "
                    "is required."
                )
            ),
            Length(
                min=10,
                max=500,
                message=(
                    "The reason must contain between "
                    "10 and 500 characters."
                ),
            ),
        ],
    )

    submit = SubmitField(
        "Reissue and Send"
    )