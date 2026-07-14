from flask_wtf import FlaskForm
from wtforms import (
    BooleanField,
    SubmitField,
    TextAreaField,
)
from wtforms.validators import (
    DataRequired,
    Length,
)


class WorkflowChecklistForm(FlaskForm):
    """
    Provides CSRF protection for the database-driven checklist.
    """

    submit = SubmitField("Submit Checklist")


class AdminApprovalForm(FlaskForm):
    """
    Final administrative approval form.

    Admin must explicitly confirm that the previous departmental
    clearances have been reviewed.
    """

    clearance_confirmed = BooleanField(
        (
            "I confirm that all previous departmental clearances "
            "have been reviewed and completed."
        ),
        validators=[
            DataRequired(
                message=(
                    "You must confirm that the previous clearances "
                    "have been reviewed."
                )
            )
        ],
    )

    remarks = TextAreaField(
        "Final Approval Remarks",
        validators=[
            Length(
                max=2000,
                message=(
                    "Approval remarks cannot exceed "
                    "2000 characters."
                ),
            )
        ],
    )

    submit = SubmitField("Approve and Close Case")