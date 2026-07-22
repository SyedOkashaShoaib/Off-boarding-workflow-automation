NAMING_CONVENTION = {
    "ix": "ix_%(table_name)s_%(column_0_name)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": (
        "fk_%(table_name)s_%(column_0_name)s_"
        "%(referred_table_name)s"
    ),
    "pk": "pk_%(table_name)s",
}


def upgrade():
    with op.batch_alter_table(
        "checklist_responses",
        schema=None,
        naming_convention=NAMING_CONVENTION,
    ) as batch_op:
        batch_op.alter_column(
            "not_applicable_reason",
            new_column_name="response_reason",
            existing_type=sa.Text(),
            existing_nullable=True,
        )

        batch_op.add_column(
            sa.Column(
                "responsible_employee_id",
                sa.Integer(),
                nullable=False,
            )
        )

        batch_op.create_index(
            "ix_checklist_responses_responsible_employee_id",
            ["responsible_employee_id"],
            unique=False,
        )

        batch_op.create_foreign_key(
            (
                "fk_checklist_responses_"
                "responsible_employee_id_"
                "department_employees"
            ),
            "department_employees",
            ["responsible_employee_id"],
            ["id"],
        )


def downgrade():
    with op.batch_alter_table(
        "checklist_responses",
        schema=None,
        naming_convention=NAMING_CONVENTION,
    ) as batch_op:
        batch_op.drop_constraint(
            (
                "fk_checklist_responses_"
                "responsible_employee_id_"
                "department_employees"
            ),
            type_="foreignkey",
        )

        batch_op.drop_index(
            "ix_checklist_responses_responsible_employee_id"
        )

        batch_op.drop_column(
            "responsible_employee_id"
        )

        batch_op.alter_column(
            "response_reason",
            new_column_name="not_applicable_reason",
            existing_type=sa.Text(),
            existing_nullable=True,
        )