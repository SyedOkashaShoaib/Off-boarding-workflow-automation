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
       