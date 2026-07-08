from app.extension import db, migrate
from datetime import datetime, timezone

class Offboarding_Case(db.Model):
    __tablename__ = 'offboarding_case'

    id = db.Column(db.Integer, primary_key = True)
    case_number = db.Column(db.String(30), nullable=False, unique=True)
    emp_name = db.Column(db.String(70), nullable=False) 
    emp_id = db.Column(db.Integer, nullable=False, unique=True)
    emp_designation = db.Column(db.String, nullable=False)
    emp_department = db.Column(db.String, nullable=False)
    last_day = db.Column(db.Date, nullable=False)
    line_manager = db.Column(db.String(70), nullable=False) #should this be a string, or a drop down with predefined values s
    # created_by = db.Column(db.String(70), nullable=True)
    status = db.Column(db.String(30), default='CREATED') #add a check to define the domain of status laterr
    created_at = db.Column(db.DateTime(timezone=True), default=lambda:datetime.now(timezone.utc),
                           onupdate=lambda:datetime.now(timezone.utc))
    


class Department(db.Model):
    __tablename__ = 'department'
    dep_id= db.Column(db.Integer, primary_key = True)
    dep_name=db.Column(db.String(70), nullable=False, unique=True)

class ChecklistItem(db.Model):
    __tablename__ = 'checklist_item'
    item_id = db.Column(db.Integer, primary_key=True)
    
