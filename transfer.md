from datetime import datetime, timedelta, timezone
from flask_login import UserMixin
from app.extension import db
from sqlalchemy.orm import validates
from werkzeug.security import (
    check_password_hash,
    generate_password_hash,
)


def utc_now():
    return datetime.now(timezone.utc)

ROLE_NOC_OPERATOR = "NOC_OPERATOR"
ROLE_FINAL_APPROVER = 'FINAL_APPROVER'
ROLE_SYSTEM_ADMIN = 'SYSTEM_ADMIN'

PORTAL_ROLES = (
    ROLE_NOC_OPERATOR,
    ROLE_FINAL_APPROVER,
    ROLE_SYSTEM_ADMIN,
)
class DepartmentEmployee(db.Model):
    """
    Employee available for selection as the person responsible
    for an individual departmental checklist item.
    """

    __tablename__ = "department_employees"

    __table_args__ = (
        db.Index(
            "ix_department_employees_department_active",
            "department_id",
            "is_active",
        ),
    )

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    department_id = db.Column(
        db.Integer,
        db.ForeignKey("departments.id"),
        nullable=False,
    )

    employee_code = db.Column(
        db.String(50),
        unique=True,
        nullable=False,
        index=True,
    )

    full_name = db.Column(
        db.String(150),
        nullable=False,
    )

    is_active = db.Column(
        db.Boolean,
        default=True,
        nullable=False,
    )

    department = db.relationship(
        "Department",
        back_populates="employees",
    )

    def __repr__(self):
        return (
            f"<DepartmentEmployee "
            f"{self.employee_code} "
            f"{self.full_name}>"
        )

class User(UserMixin, db.Model):
    """
    Authenticated portal user.

    Departmental task recipients will use separate task-specific
    access grants later and are not represented by this model unless
    they are also authorised portal users.
    """

    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    email = db.Column(
        db.String(254),
        unique=True,
        nullable=False,
        index=True,
    )

    full_name = db.Column(
        db.String(150),
        nullable=False,
    )

    password_hash = db.Column(
        db.String(512),
        nullable=False,
    )

    role = db.Column(
        db.String(50),
        nullable=False,
        default=ROLE_NOC_OPERATOR,
    )

    active = db.Column(
        db.Boolean,
        nullable=False,
        default=True,
    )

    last_login_at = db.Column(
        db.DateTime(timezone=True),
        nullable=True,
    )

    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=utc_now,
    )

    updated_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=utc_now,
        onupdate=utc_now,
    )

    @property
    def is_active(self) -> bool:
        """
        Flask-Login uses this property to determine whether the
        account is permitted to establish an authenticated session.
        """

        return bool(self.active)

    @staticmethod
    def normalize_email(value: str) -> str:
        """
        Return the canonical representation used for login and
        uniqueness checks.
        """

        return str(value or "").strip().lower()

    @validates("email")
    def validate_email(
        self,
        key: str,
        value: str,
    ) -> str:
        """
        Normalize portal email addresses before persistence.
        """

        normalized_email = self.normalize_email(value)

        if not normalized_email:
            raise ValueError(
                "A portal user email address is required."
            )

        return normalized_email

    @validates("role")
    def validate_role(
        self,
        key: str,
        value: str,
    ) -> str:
        """
        Reject unsupported portal roles.
        """

        normalized_role = str(value or "").strip().upper()

        if normalized_role not in PORTAL_ROLES:
            raise ValueError(
                f"Unsupported portal role: {normalized_role}"
            )

        return normalized_role

    def set_password(
        self,
        password: str,
    ) -> None:
        """
        Hash and store a plaintext password.

        Plaintext passwords must never be stored in the database.
        """

        if not password:
            raise ValueError(
                "A password is required."
            )

        self.password_hash = generate_password_hash(
            password
        )

    def check_password(
        self,
        password: str,
    ) -> bool:
        """
        Compare a submitted password with the stored hash.
        """

        if not password or not self.password_hash:
            return False

        return check_password_hash(
            self.password_hash,
            password,
        )

    def has_role(
        self,
        *roles: str,
    ) -> bool:
        """
        Return whether this user has one of the supplied roles.
        """

        normalized_roles = {
            str(role).strip().upper()
            for role in roles
        }

        return self.role in normalized_roles

    def __repr__(self) -> str:
        return (
            f"<User id={self.id} "
            f"email={self.email!r} "
            f"role={self.role!r}>"
        )
class Department(db.Model):
    __tablename__ = "departments"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(150), nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    phases = db.relationship("WorkflowPhase", back_populates="department")
    employees = db.relationship("DepartmentEmployee", back_populates='department', 
                                order_by='DepartmentEmployee.full_name', )

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
    __table_args__=(
        db.Index(
        "ix_offboarding_case_status_updated_at",
        "status",
        "updated_at",
    ),
        db.Index(
            "ix_offboarding_case_current_phase_status",
            "current_phase_id",
            "status",
        ),
        db.Index(
            "ix_offboarding_case_employee_id",
            "employee_id",
        ),

    )
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
    __table_args__= (
        db.UniqueConstraint(
            "case_id",
            "phase_id",
            name="uq_workflow_tasks_case_phase",
        ),
        db.Index(
            "ix_workflow_tasks_status_due_at",
            "status",
            "due_at",
        ),
        
    )
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
    notifications= db.relationship(
        "EmailNotification", 
        back_populates='workflow_task', 
        cascade='all, delete-orphan')
    access_grants = db.relationship(
    "TaskAccessGrant",
    back_populates="workflow_task",
    cascade="all, delete-orphan",
)
    def __repr__(self):
        return f"<WorkflowTask Case={self.case_id} Phase={self.phase_id} Status={self.status}>"
class TaskAccessGrant(db.Model):
    """
    Secure access grant for one departmental workflow task.

    The raw token is sent through email but is never stored in the
    database. Only its SHA-256 digest is persisted.
    """

    __tablename__ = "task_access_grants"

    __table_args__ = (
        db.Index(
            "ix_task_access_grants_task_state",
            "workflow_task_id",
            "revoked_at",
            "consumed_at",
        ),
    )

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    workflow_task_id = db.Column(
        db.Integer,
        db.ForeignKey("workflow_tasks.id"),
        nullable=False,
    )

    token_hash = db.Column(
        db.String(64),
        unique=True,
        nullable=False,
    )

    recipient_email = db.Column(
        db.String(254),
        nullable=False,
    )

    expires_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
    )

    created_at = db.Column(
        db.DateTime(timezone=True),
        default=utc_now,
        nullable=False,
    )

    last_accessed_at = db.Column(
        db.DateTime(timezone=True),
        nullable=True,
    )

    access_count = db.Column(
        db.Integer,
        nullable=False,
        default=0,
    )

    consumed_at = db.Column(
        db.DateTime(timezone=True),
        nullable=True,
    )

    revoked_at = db.Column(
        db.DateTime(timezone=True),
        nullable=True,
    )

    workflow_task = db.relationship(
        "WorkflowTask",
        back_populates="access_grants",
    )

    def __repr__(self):
        return (
            f"<TaskAccessGrant id={self.id} "
            f"task={self.workflow_task_id}>"
        )

class ChecklistResponse(db.Model):
    """
    Recorded response for one checklist item within one workflow
    task.
    """

    __tablename__ = "checklist_responses"

    __table_args__ = (
        db.UniqueConstraint(
            "workflow_task_id",
            "checklist_item_id",
            name="uq_task_checklist_item_response",
        ),
    )

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    case_id = db.Column(
        db.Integer,
        db.ForeignKey("offboarding_cases.id"),
        nullable=False,
    )

    workflow_task_id = db.Column(
        db.Integer,
        db.ForeignKey("workflow_tasks.id"),
        nullable=False,
    )

    checklist_item_id = db.Column(
        db.Integer,
        db.ForeignKey("checklist_items.id"),
        nullable=False,
    )

    responsible_employee_id = db.Column(
        db.Integer,
        db.ForeignKey("department_employees.id"),
        nullable=False,
        index=True,
    )

    response_status = db.Column(
        db.String(50),
        nullable=False,
    )

    response_reason = db.Column(
        db.Text,
        nullable=True,
    )

    responded_by = db.Column(
        db.String(150),
        nullable=True,
    )

    responded_at = db.Column(
        db.DateTime(timezone=True),
        default=utc_now,
        nullable=False,
    )

    workflow_task = db.relationship(
        "WorkflowTask",
        back_populates="responses",
    )

    checklist_item = db.relationship(
        "ChecklistItem",
        back_populates="responses",
    )

    responsible_employee = db.relationship(
        "DepartmentEmployee",
       back_populates="responses",
    )
    @property
    def not_applicable_reason(self):
        return self.response_reason
    
    @not_applicable_reason.setter
    def not_applicable_reason(self, value):
        self.response_reason=value

    def __repr__(self):
        return f"<ChecklistResponse Task={self.workflow_task_id} Item={self.checklist_item_id}>"


class AuditLog(db.Model):
    __tablename__ = "audit_logs"
    __table_args__ = (
        db.Index(
            "ix_audit_log_case_created_at",
            "case_id",
            "created_at",
        ),
    )
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
    

class EmailNotification(db.Model):
    __tablename__ = 'email_notifications'
    __table_args__=(
        db.Index("ix_email_notifications_case_status",
                 "case_id",
                 "status",),
        db.Index("ix_email_notifications_task_type",
                 "workflow_task_id",
                 "notification_type",),
    )
    id = db.Column(db.Integer, primary_key=True)
    case_id = db.Column(db.Integer, db.ForeignKey('offboarding_cases.id'), nullable=False)
    workflow_task_id = db.Column(db.Integer, db.ForeignKey('workflow_tasks.id'), nullable=False)
    notification_type = db.Column(db.String(50), nullable=False, default='TASK_ASSIGNED')
    deduplication_key = db.Column(db.String(255), unique= True, nullable=True)
    recipient_email = db.Column(db.String(150), nullable=False)
    subject = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(30), nullable=False, default='PENDING')
    provider_message_id = db.Column(db.String(255), nullable=True)
    error_message = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), default = utc_now, nullable=False)
    attempted_at = db.Column(db.DateTime(timezone=True), nullable=True)
    sent_at = db.Column(db.DateTime(timezone=True), nullable=True)
    case = db.relationship("OffboardingCase")
    workflow_task = db.relationship("WorkflowTask", back_populates='notifications')

    def __repr__(self):
        return (
            f"EmailNotification"
            f"Task={self.workflow_task_id}"
            f"Status={self.status}"
        )


    (.venv) PS C:\Users\intern\Desktop\intern_summer_26\offboarding_workflow> Remove-Item "C:\Users\intern\Desktop\intern_summer_26\offboarding_workflow\instance\offboarding.db"
(.venv) PS C:\Users\intern\Desktop\intern_summer_26\offboarding_workflow> flask --app run.py db upgrade
INFO  [alembic.runtime.migration] Context impl SQLiteImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> 094f31a0b566, freshhh
INFO  [alembic.runtime.migration] Running upgrade 094f31a0b566 -> 0d2eb512e3b1, added emailnotification class
INFO  [alembic.runtime.migration] Running upgrade 0d2eb512e3b1 -> 905ff896573a, fixed version bug and added email notification class
INFO  [alembic.runtime.migration] Running upgrade 905ff896573a -> b8c3e036fdd3, add deduplication key column
INFO  [alembic.runtime.migration] Running upgrade b8c3e036fdd3 -> 72ca45eb4245, add indexes
INFO  [alembic.runtime.migration] Running upgrade 72ca45eb4245 -> 6e49f821eca5, correct index name
INFO  [alembic.runtime.migration] Running upgrade 6e49f821eca5 -> 066ccd71be93, auth portal users
INFO  [alembic.runtime.migration] Running upgrade 066ccd71be93 -> 0dace7b106cf, Add secure dep task access grants
INFO  [alembic.runtime.migration] Running upgrade 0dace7b106cf -> dfef771cf82e, add department employee directory
INFO  [alembic.runtime.migration] Running upgrade dfef771cf82e -> 430e02d26f99, update checklist reposnse accountability
Traceback (most recent call last):
  File "C:\Users\intern\AppData\Local\Programs\Python\Python39\lib\runpy.py", line 197, in _run_module_as_main
    return _run_code(code, main_globals, None,
  File "C:\Users\intern\AppData\Local\Programs\Python\Python39\lib\runpy.py", line 87, in _run_code
    exec(code, run_globals)
  File "C:\Users\intern\Desktop\intern_summer_26\offboarding_workflow\.venv\Scripts\flask.exe\__main__.py", line 5, in <module>
  File "C:\Users\intern\Desktop\intern_summer_26\offboarding_workflow\.venv\lib\site-packages\flask\cli.py", line 1131, in main
    cli.main()
  File "C:\Users\intern\Desktop\intern_summer_26\offboarding_workflow\.venv\lib\site-packages\click\core.py", line 1082, in main
    rv = self.invoke(ctx)
  File "C:\Users\intern\Desktop\intern_summer_26\offboarding_workflow\.venv\lib\site-packages\click\core.py", line 1697, in invoke
    return _process_result(sub_ctx.command.invoke(sub_ctx))
  File "C:\Users\intern\Desktop\intern_summer_26\offboarding_workflow\.venv\lib\site-packages\click\core.py", line 1697, in invoke
    return _process_result(sub_ctx.command.invoke(sub_ctx))
  File "C:\Users\intern\Desktop\intern_summer_26\offboarding_workflow\.venv\lib\site-packages\click\core.py", line 1443, in invoke
    return ctx.invoke(self.callback, **ctx.params)
  File "C:\Users\intern\Desktop\intern_summer_26\offboarding_workflow\.venv\lib\site-packages\click\core.py", line 788, in invoke
    return __callback(*args, **kwargs)
  File "C:\Users\intern\Desktop\intern_summer_26\offboarding_workflow\.venv\lib\site-packages\click\decorators.py", line 33, in new_func    
    return f(get_current_context(), *args, **kwargs)
  File "C:\Users\intern\Desktop\intern_summer_26\offboarding_workflow\.venv\lib\site-packages\flask\cli.py", line 400, in decorator
    return ctx.invoke(f, *args, **kwargs)
  File "C:\Users\intern\Desktop\intern_summer_26\offboarding_workflow\.venv\lib\site-packages\click\core.py", line 788, in invoke
    return __callback(*args, **kwargs)
  File "C:\Users\intern\Desktop\intern_summer_26\offboarding_workflow\.venv\lib\site-packages\flask_migrate\cli.py", line 157, in upgrade   
    _upgrade(directory or g.directory, revision, sql, tag, x_arg or g.x_arg)
  File "C:\Users\intern\Desktop\intern_summer_26\offboarding_workflow\.venv\lib\site-packages\flask_migrate\__init__.py", line 111, in wrapped
    f(*args, **kwargs)
  File "C:\Users\intern\Desktop\intern_summer_26\offboarding_workflow\.venv\lib\site-packages\flask_migrate\__init__.py", line 200, in upgrade
    command.upgrade(config, revision, sql=sql, tag=tag)
  File "C:\Users\intern\Desktop\intern_summer_26\offboarding_workflow\.venv\lib\site-packages\alembic\command.py", line 483, in upgrade     
    script.run_env()
  File "C:\Users\intern\Desktop\intern_summer_26\offboarding_workflow\.venv\lib\site-packages\alembic\script\base.py", line 549, in run_env
    util.load_python_file(self.dir, "env.py")
  File "C:\Users\intern\Desktop\intern_summer_26\offboarding_workflow\.venv\lib\site-packages\alembic\util\pyfiles.py", line 116, in load_python_file
    module = load_module_py(module_id, path)
  File "C:\Users\intern\Desktop\intern_summer_26\offboarding_workflow\.venv\lib\site-packages\alembic\util\pyfiles.py", line 136, in load_module_py
    spec.loader.exec_module(module)  # type: ignore
  File "<frozen importlib._bootstrap_external>", line 850, in exec_module
  File "<frozen importlib._bootstrap>", line 228, in _call_with_frames_removed
  File "migrations\env.py", line 113, in <module>
    run_migrations_online()
  File "migrations\env.py", line 107, in run_migrations_online
    context.run_migrations()
  File "<string>", line 8, in run_migrations
  File "C:\Users\intern\Desktop\intern_summer_26\offboarding_workflow\.venv\lib\site-packages\alembic\runtime\environment.py", line 946, in 
run_migrations
    self.get_context().run_migrations(**kw)
  File "C:\Users\intern\Desktop\intern_summer_26\offboarding_workflow\.venv\lib\site-packages\alembic\runtime\migration.py", line 627, in run_migrations
    step.migration_fn(**kw)
  File "C:\Users\intern\Desktop\intern_summer_26\offboarding_workflow\migrations\versions\430e02d26f99_update_checklist_reposnse_accountability.py", line 26, in upgrade
    batch_op.drop_column('not_applicable_reason')
  File "C:\Users\intern\AppData\Local\Programs\Python\Python39\lib\contextlib.py", line 126, in __exit__
    next(self.gen)
  File "C:\Users\intern\Desktop\intern_summer_26\offboarding_workflow\.venv\lib\site-packages\alembic\operations\base.py", line 397, in batch_alter_table
    impl.flush()
  File "C:\Users\intern\Desktop\intern_summer_26\offboarding_workflow\.venv\lib\site-packages\alembic\operations\batch.py", line 161, in flush
    fn(*arg, **kw)
  File "C:\Users\intern\Desktop\intern_summer_26\offboarding_workflow\.venv\lib\site-packages\alembic\operations\batch.py", line 670, in add_constraint
    raise ValueError("Constraint must have a name")
ValueError: Constraint must have a name
