from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, IntegerField, DateField
from wtforms.validators import DataRequired, Length


def strip_whitespace(value):
    if isinstance(value, str):
        return value.strip()
    return value
class Case_Form(FlaskForm):
    emp_name = StringField(label='Employee name', validators=[DataRequired(message="Employee name is required")] )
    # emp_id = IntegerField('Employe')
    emp_desig = StringField(label="Employee designation", validators=[DataRequired(message='Employee Designation is required')])
    emp_dep = StringField(label="Employee department", validators=[DataRequired(message='Employee department is required')])
    last_date = DateField(label="Employee's last date of work", validators=[DataRequired(message='Last date of working si required')])
    emp_id = StringField(label='Employee id',filters=[strip_whitespace], validators=[DataRequired(message='Employee id is required'), Length(max=50, message=("EMployee id cannot exceed 50 characters"))])
    line_manager = StringField(label="Line manager/HOD", validators=[DataRequired(message='Employee id is required')])
    submit = SubmitField("Begin Offboarding Process")

