from app.extension import db, migrate


class Offboarding_Case(db.Model):
    __tablename__ = 'offboarding_case'

    id = db.Column(db.Integer, primary_key = True)
    case_number = db.Column(db.String(30), nullable=False, unique=True)
    emp_name = db.Column(db.String(70), nullable=False) 
    emp_id = db.Column(db.Integer, nullable=False, unique=True)
    emp_designation = db.Column(db.String, nullable=False)
    emp_department = db.Column(db.String, nullable=False)
    last_day = db.Column(db.Date, nullable=False)
    line_manager = db.Column(db.String(70), nullable=False)
    created_by = db.Column(db.String(70), nullable=False)


