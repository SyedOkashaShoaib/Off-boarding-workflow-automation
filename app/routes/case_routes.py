from app.extension import db
from flask import Blueprint, render_template, redirect, url_for, flash
from app.forms.offboarding_case import Case_Form
from sqlalchemy.exc import SQLAlchemyError
from app.models import OffboardingCase
from datetime import datetime, timezone
from app.services.workflow_service import create_initial_workflow_task, WorkflowConfigurationError, WorkflowTask

case_bp = Blueprint('cases', __name__)
main_bp = Blueprint('main', __name__)

def generate_Case_Number():
    last_id = OffboardingCase.query.order_by(OffboardingCase.id.desc()).first()
    if last_id is None:
        next_id = 1
    else:
        next_id = last_id.id + 1

    return f"CASE_{next_id}"

@case_bp.route('/create', 
methods=['GET', 'POST'])
def create_Case():
    form = Case_Form()
    if form.validate_on_submit():
        try:
            case_id = generate_Case_Number()
            new_case = OffboardingCase(
                case_number=case_id, employee_name = form.emp_name.data,
                employee_id = form.emp_id.data, designation = form.emp_desig.data,
                department = form.emp_dep.data, last_working_day = form.last_date.data,
                line_manager = form.line_manager.data,
                status = 'CREATED', #i dont want these values to eb hardcoded. WIll figure out a way (not that hard) to make this dynamic.
                created_by = 'NOC'
                )
            db.session.add(new_case)
            new_task = create_initial_workflow_task(new_case)
            db.session.add(new_task)
            db.session.commit()
            flash(f"New offloading case {new_case.case_number} has been created.", "SUCCESS")
            flash(f"{new_case.case_number} has been assigned to {new_task.assigned_to_email}.", "SUCCESS")
            return redirect(url_for('cases.case_created', case_id = new_case.id))
        
        except WorkflowConfigurationError as e:
            db.session.rollback()
            flash(f"The case could not be created due to the error: {e}", "WORKFLOW CONFIG. ERROR")
        except SQLAlchemyError as e:
            db.session.rollback()
            flash(f"THe case could not be created due to a database error", "DATABASE ERROR")

    return render_template('create_case.html', form=form)

@case_bp.route("/<int:case_id>/created")
def case_created(case_id):
    case=OffboardingCase.query.get_or_404(case_id)
    initial_task = WorkflowTask.query.filter_by(case_id=case_id).order_by(WorkflowTask.assigned_at.asc()).first_or_404()
    return render_template('case_created.html', case=case, task=initial_task, notification_status='not sent')