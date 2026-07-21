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