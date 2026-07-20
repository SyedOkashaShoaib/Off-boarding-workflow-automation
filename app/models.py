from datetime import datetime, timedelta, timezone

from app.extension import db


def utc_now():
    return datetime.now(timezone.utc)


class Department(db.Model):
    __tablename__ = "departments"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(150), nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    phases = db.relationship("WorkflowPhase", back_populates="department")

    def __repr__(self):
        return f"<Department {self.name}>"


class WorkflowPhase(db.Model):
    __tablename__ = "workflow_phases"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    slug = db.Column(db.String(100), unique=True, nullable=False)   

    department_id = db.Column(
        db.Integer,
        db.ForeignKey("departments.id"),
        nullable=False
    )

    phase_order = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=True)
    is_final_approval = db.Column(db.Boolean, default=False, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    department = db.relationship("Department", back_populates="phases")

    checklist_items = db.relationship(
        "ChecklistItem",
        back_populates="phase",
        order_by="ChecklistItem.display_order",
        cascade="all, delete-orphan"
    )

    tasks = db.relationship("WorkflowTask", back_populates="phase")

    def __repr__(self):
        return f"<WorkflowPhase {self.phase_order} - {self.name}>"


class ChecklistItem(db.Model):
    __tablename__ = "checklist_items"

    id = db.Column(db.Integer, primary_key=True)

    phase_id = db.Column(
        db.Integer,
        db.ForeignKey("workflow_phases.id"),
        nullable=False
    )

    section = db.Column(db.String(150), nullable=True)
    item_text = db.Column(db.Text, nullable=False)
    display_order = db.Column(db.Integer, nullable=False)

    is_required = db.Column(db.Boolean, default=True, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    phase = db.relationship("WorkflowPhase", back_populates="checklist_items")
    responses = db.relationship("ChecklistResponse", back_populates="checklist_item")

    def __repr__(self):
        return f"<ChecklistItem {self.item_text[:40]}>"


class OffboardingCase(db.Model):
    __tablename__ = "offboarding_cases"

    id = db.Column(db.Integer, primary_key=True)

    case_number = db.Column(db.String(50), unique=True, nullable=False)

    employee_name = db.Column(db.String(150), nullable=False)
    employee_id = db.Column(db.String(50), nullable=False)

    designation = db.Column(db.String(150), nullable=False)
    department = db.Column(db.String(150), nullable=False)
    last_working_day = db.Column(db.Date, nullable=False)

    line_manager = db.Column(db.String(150), nullable=False)

    status = db.Column(db.String(50), nullable=False, default="CREATED")

    current_phase_id = db.Column(
        db.Integer,
        db.ForeignKey("workflow_phases.id"),
        nullable=True
    )

    created_by = db.Column(db.String(150), nullable=True)

    created_at = db.Column(
        db.DateTime(timezone=True),
        default=utc_now,
        nullable=False
    )

    updated_at = db.Column(
        db.DateTime(timezone=True),
        default=utc_now,
        onupdate=utc_now,
        nullable=False
    )

    closed_at = db.Column(db.DateTime(timezone=True), nullable=True)

    current_phase = db.relationship(
        "WorkflowPhase",
        foreign_keys=[current_phase_id]
    )

    tasks = db.relationship(
        "WorkflowTask",
        back_populates="case",
        cascade="all, delete-orphan"
    )

    audit_logs = db.relationship(
        "AuditLog",
        back_populates="case",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<OffboardingCase {self.case_number} - {self.employee_name}>"


class WorkflowTask(db.Model):
    __tablename__ = "workflow_tasks"

    id = db.Column(db.Integer, primary_key=True)

    case_id = db.Column(
        db.Integer,
        db.ForeignKey("offboarding_cases.id"),
        nullable=False
    )

    phase_id = db.Column(
        db.Integer,
        db.ForeignKey("workflow_phases.id"),
        nullable=False
    )

    assigned_to_email = db.Column(db.String(150), nullable=False)
    status = db.Column(db.String(50), nullable=False, default="PENDING")

    assigned_at = db.Column(
        db.DateTime(timezone=True),
        default=utc_now,
        nullable=False
    )

    due_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: utc_now() + timedelta(days=7),
        nullable=False
    )

    opened_at = db.Column(db.DateTime(timezone=True), nullable=True)
    submitted_at = db.Column(db.DateTime(timezone=True), nullable=True)

    case = db.relationship("OffboardingCase", back_populates="tasks")
    phase = db.relationship("WorkflowPhase", back_populates="tasks")

    responses = db.relationship(
        "ChecklistResponse",
        back_populates="workflow_task",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<WorkflowTask Case={self.case_id} Phase={self.phase_id} Status={self.status}>"


class ChecklistResponse(db.Model):
    __tablename__ = "checklist_responses"

    id = db.Column(db.Integer, primary_key=True)

    case_id = db.Column(
        db.Integer,
        db.ForeignKey("offboarding_cases.id"),
        nullable=False
    )

    workflow_task_id = db.Column(
        db.Integer,
        db.ForeignKey("workflow_tasks.id"),
        nullable=False
    )

    checklist_item_id = db.Column(
        db.Integer,
        db.ForeignKey("checklist_items.id"),
        nullable=False
    )

    response_status = db.Column(db.String(50), nullable=False)
    not_applicable_reason = db.Column(db.Text, nullable=True)

    responded_by = db.Column(db.String(150), nullable=True)

    responded_at = db.Column(
        db.DateTime(timezone=True),
        default=utc_now,
        nullable=False
    )

    workflow_task = db.relationship("WorkflowTask", back_populates="responses")
    checklist_item = db.relationship("ChecklistItem", back_populates="responses")

    __table_args__ = (
        db.UniqueConstraint(
            "workflow_task_id",
            "checklist_item_id",
            name="uq_task_checklist_item_response"
        ),
    )

    def __repr__(self):
        return f"<ChecklistResponse Task={self.workflow_task_id} Item={self.checklist_item_id}>"


class AuditLog(db.Model):
    __tablename__ = "audit_logs"

    id = db.Column(db.Integer, primary_key=True)

    case_id = db.Column(
        db.Integer,
        db.ForeignKey("offboarding_cases.id"),
        nullable=False
    )

    action = db.Column(db.String(150), nullable=False)
    performed_by = db.Column(db.String(150), nullable=True)
    details = db.Column(db.Text, nullable=True)

    created_at = db.Column(
        db.DateTime(timezone=True),
        default=utc_now,
        nullable=False
    )

    case = db.relationship("OffboardingCase", back_populates="audit_logs")

    def __repr__(self):
        return f"<AuditLog {self.action}>"