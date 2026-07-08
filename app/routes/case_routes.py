from app.extension import db
from flask import Blueprint
from flask import render_template, redirect, url_for, flash
from app.forms.offboarding_case import Case_Form
from app.extension import db
# from sqlalchemy import select
from app.models import Offboarding_Case
case_bp = Blueprint('case_bp', __name__, static_folder='static', template_folder='templates', url_prefix='/case')

def generate_Case_Number():
    last_id = Offboarding_Case.query.order_by(Offboarding_Case.id.desc()).first()
    if last_id is None:
        last_id = 1
    else:
        last_id = last_id + 1

    return f"CASE_{last_id}"
#figure out the logic of generating case number.


@case_bp.route('/create', 
methods=['GET', 'POST'])
def create_Case():
    form = Case_Form()
    if form.validate_on_submit():
        case_id = generate_Case_Number()
        new_case = Case_Form(
            case_number=case_id, emp_name = form.emp_name.data,
            emp_id = form.emp_id.data, emp_designation = form.emp_desig.data,
            emp_department = form.emp_dep.data, last_day = form.last_date.data,
            line_manager = form.line_manager.data
            )
        db.session.add(new_case)
        db.session.commit()
        flash("New offloading case created succesfully.")
        #further logic
    return render_template('create_case', form)


    # id = db.Column(db.Integer, primary_key = True)
    # case_number = db.Column(db.String(30), nullable=False, unique=True)
    # emp_name = db.Column(db.String(70), nullable=False) 
    # emp_id = db.Column(db.Integer, nullable=False, unique=True)
    # emp_designation = db.Column(db.String, nullable=False)
    # emp_department = db.Column(db.String, nullable=False)
    # last_day = db.Column(db.Date, nullable=False)
    # line_manager = db.Column(db.String(70), nullable=False)
    # created_by = db.Column(db.String(70), nullable=False)
    #    status = db.Column(db.String(30), default='CREATED') #add a check to define the domain of status laterr
    # created_at = db.Column(db.DateTime(timezone=True), default=lambda:datetime.now(timezone.utc),
    #                        onupdate=lambda:datetime.now(timezone.utc))
    #     <p>
    #     {{ form.emp_name.label }}<br>
    #     {{ form.emp_name(size=32) }}
    # </p>
    # <p>
    #     {{ form.emp_desig.label }}<br>
    #     {{ form.emp_desig(size=32) }}
    # </p>
    # <p>
    #     {{ form.emp_dep.label }}<br>
    #     {{ form.emp_dep(size=32) }}
    # </p>
    # <p>
    #     {{ form.last_date.label }}<br>
    #     {{ form.last_date }}
    # </p>
    # <p>{{ form.submit() }}</p>