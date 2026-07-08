from app.extension import db
from models import Offboarding_Case
from flask import Blueprint
from flask import render_template, redirect, url_for, flash
from app.forms import LoginForm
from app.extension import db
from app.routes import Case_Form
# from sqlalchemy import select
from app.models import Offboarding_Case
case_bp = Blueprint('case_bp', __name__, static_folder='static', template_folder='templates', url_prefix='case')

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

    return render_template('create_case', form)