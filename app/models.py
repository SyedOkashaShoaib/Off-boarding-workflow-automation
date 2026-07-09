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
    dep_name=db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False)


class ChecklistItem(db.Model):
    __tablename__ = 'checklist_item'
    item_id = db.Column(db.Integer, primary_key=True)
    item_text = db.Column(db.String(150), nullable=False)
    phase_id = db.Column(db.Integer, db.ForeignKey('workflow_phase.phase_id'), nullable=False)
    display_order = db.Column(db.Integer, nullable=False)
    phase = db.relationship('WorkflowPhase', back_populates='checklist_items')
    
class WorkflowPhase(db.Model):
    __tablename__ = 'workflow_phase'
    phase_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    dep_id=db.Column(db.Integer, db.ForeignKey('department.dep_id'), nullable=False)
    phase_order=db.Column(db.Integer, nullable=False) 
    checklist_items = db.relationship(ChecklistItem, back_populates='phase', order_by='ChecklistItem.display_order')

