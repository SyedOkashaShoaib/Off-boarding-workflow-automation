from app.extension import db
from flask import Blueprint
from flask import render_template, redirect, url_for, flash
from app.forms.offboarding_case import Case_Form
from app.extension import db
# from sqlalchemy import select
from app.models import Offboarding_Case

case_bp = Blueprint('cases', __name__)
main_bp = Blueprint('main', __name__)

def generate_Case_Number():
    last_id = Offboarding_Case.query.order_by(Offboarding_Case.id.desc()).first()
    if last_id is None:
        last_id = 1
    else:
        last_id = last_id + 1

    return f"CASE_{last_id}"
#figure out the logic of generating case number.

@main_bp.route('/')
def home():
    return redirect (url_for('cases.create_Case'))

@case_bp.route('/create', 
methods=['GET', 'POST'])
def create_Case():
    form = Case_Form()
    if form.validate_on_submit():
        case_id = generate_Case_Number()
        new_case = Offboarding_Case(
            case_number=case_id, emp_name = form.emp_name.data,
            emp_id = form.emp_id.data, emp_designation = form.emp_desig.data,
            emp_department = form.emp_dep.data, last_day = form.last_date.data,
            line_manager = form.line_manager.data
            )
        db.session.add(new_case)
        db.session.commit()
        flash("New offloading case created succesfully.")
        #further logic
    return render_template('create_case.html', form=form)


