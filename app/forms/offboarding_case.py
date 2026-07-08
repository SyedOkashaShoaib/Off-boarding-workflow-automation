from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, IntegerField, DateField
from wtforms.validators import DataRequired, Length

class Case_Form(FlaskForm):
    emp_name = StringField(label='Employee name', validators=[DataRequired(message="Employee name is required")] )
    # emp_id = IntegerField('Employe')
    emp_desig = StringField(label="Employee designation", validators=[DataRequired(message='Employee Designation is required')])
    emp_dep = StringField(label="EMployee department", validators=[DataRequired(message='Employee department is required')])
    last_date = DateField(label="Select the employee's last date of work", validators=[DataRequired(message='Last date of working si required')])
    emp_id = IntegerField(label='Enter employee id',validators=[DataRequired(message='Employee id is required')])
    line_manager = StringField(label="Enter the name of line manager/HOD", validators=[DataRequired(message='Employee id is required')])
    submit = SubmitField("Begin Offboarding Process")

    # id = db.Column(db.Integer, primary_key = True)
    # case_number = db.Column(db.String(30), nullable=False, unique=True)
    # emp_name = db.Column(db.String(70), nullable=False) 
    # emp_id = db.Column(db.Integer, nullable=False, unique=True)
    # emp_designation = db.Column(db.String, nullable=False)
    # emp_department = db.Column(db.String, nullable=False)
    # last_day = db.Column(db.Date, nullable=False)
    # line_manager = db.Column(db.String(70), nullable=False)
    # created_by = db.Column(db.String(70), nullable=False)