from flask_wtf import FlaskForm
from wtforms import SubmitField

class WorkflowChecklistForm(FlaskForm):
    submit = SubmitField("Submit Checklist")