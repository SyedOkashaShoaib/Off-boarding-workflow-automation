import click
from flask.cli import with_appcontext

from app.extension import db
from app.models import( 
    ChecklistItem, 
    Department, 
    WorkflowPhase,
    DepartmentEmployee,)


@click.command("seed-data")
@with_appcontext
def seed_data_command():
    """
    Seed workflow departments, phases, and departmental checklists.

    The command is idempotent: running it repeatedly updates existing
    records rather than creating duplicates.
    """

    try:
        seed_departments()

        # Ensure newly added departments have database IDs before
        # workflow phases are created.
        db.session.flush()
        created_employee_count = (
            seed_department_employees()
        )

        seed_workflow_phases()

        # Ensure newly added phases have database IDs before
        # checklist items are created.
        db.session.flush()

        created_noc_items = seed_noc_checklist_items()
        created_mis_items = seed_mis_checklist_items()
        created_hardware_items = seed_hardware_checklist_items()

        db.session.commit()

    except Exception as exc:
        db.session.rollback()

        raise click.ClickException(
            f"Seed operation failed: {exc}"
        ) from exc

    click.echo("Seed data completed successfully.")
    click.echo("New department employees created: "
               f"{created_employee_count}")
    click.echo(
        f"New NOC checklist items created: {created_noc_items}"
    )
    click.echo(
        f"New MIS checklist items created: {created_mis_items}"
    )
    click.echo(
        "New Hardware checklist items created: "
        f"{created_hardware_items}"
    )


def seed_departments() -> None:
    """Insert or update workflow departments."""

    departments_data = [
        {
            "name": "NOC",
            "email": "intern@BarrettHodsgon.com",
        },
        {
            "name": "MIS",
            "email": "intern@BarrettHodsgon.com",
        },
        {
            "name": "Hardware",
            "email": "intern@BarrettHodsgon.com",
        },
        {
            "name": "Admin",
            "email": "intern@BarrettHodsgon.com",
        },
    ]

    for department_data in departments_data:
        department = Department.query.filter_by(
            name=department_data["name"]
        ).first()

        if department is None:
            department = Department(
                name=department_data["name"],
                email=department_data["email"],
                is_active=True,
            )

            db.session.add(department)

        else:
            department.email = department_data["email"]
            department.is_active = True
def seed_department_employees() -> int:
    """
    Insert or update prototype department employees.

    Existing employees are matched by employee code so the command
    remains safe to run repeatedly.
    """

    departments = {
        department.name: department
        for department in Department.query.all()
    }

    employees_data = [
        {
            "employee_code": "NOC-001",
            "full_name": "Sir Khurram",
            "department": "NOC",
        },
        {
            "employee_code": "NOC-002",
            "full_name": "Habib",
            "department": "NOC",
        },
                {
            "employee_code": "NOC-003",
            "full_name": "Anas",
            "department": "NOC",
        },
        {
            "employee_code": "MIS-001",
            "full_name": "MIS Officer 1",
            "department": "MIS",
        },
        {
            "employee_code": "MIS-002",
            "full_name": "MIS Officer 2",
            "department": "MIS",
        },
        {
            "employee_code": "HARDWARE-001",
            "full_name": "Hardware Officer 1",
            "department": "Hardware",
        },
        {
            "employee_code": "HARDWARE-002",
            "full_name": "Hardware Officer 2",
            "department": "Hardware",
        },
        {
            "employee_code": "ADMIN-001",
            "full_name": "Administration Officer 1",
            "department": "Admin",
        },
        {
            "employee_code": "ADMIN-002",
            "full_name": "Administration Officer 2",
            "department": "Admin",
        },
    ]

    created_count = 0

    for employee_data in employees_data:
        department = departments.get(
            employee_data["department"]
        )

        if department is None:
            raise ValueError(
                "Required department not found: "
                f"{employee_data['department']}"
            )

        employee = (
            DepartmentEmployee.query
            .filter_by(
                employee_code=(
                    employee_data["employee_code"]
                )
            )
            .first()
        )

        if employee is None:
            employee = DepartmentEmployee(
                employee_code=(
                    employee_data["employee_code"]
                ),
                full_name=(
                    employee_data["full_name"]
                ),
                department=department,
                is_active=True,
            )

            db.session.add(employee)
            created_count += 1

        else:
            employee.full_name = (
                employee_data["full_name"]
            )

            employee.department = department
            employee.is_active = True

    return created_count

def seed_workflow_phases() -> None:
    """Insert or update the ordered workflow phases."""

    departments = {
        department.name: department
        for department in Department.query.all()
    }

    phases_data = [
        {
            "name": "NOC Access & Security Clearance",
            "slug": "noc-access-security-clearance",
            "department": "NOC",
            "phase_order": 1,
            "description": (
                "Merged NOC phase covering identity, access, "
                "communication, and security clearance."
            ),
            "is_final_approval": False,
        },
        {
            "name": "MIS Business Applications Clearance",
            "slug": "mis-business-applications-clearance",
            "department": "MIS",
            "phase_order": 2,
            "description": (
                "Clearance of business applications, internal "
                "systems, and software access."
            ),
            "is_final_approval": False,
        },
        {
            "name": "Hardware & Asset Recovery",
            "slug": "hardware-asset-recovery",
            "department": "Hardware",
            "phase_order": 3,
            "description": (
                "Recovery of company hardware, accessories, "
                "and assigned physical assets."
            ),
            "is_final_approval": False,
        },
        {
            "name": "Admin Final Approval",
            "slug": "admin-final-approval",
            "department": "Admin",
            "phase_order": 4,
            "description": (
                "Final administrative approval before closing "
                "the offboarding case."
            ),
            "is_final_approval": True,
        },
    ]

    for phase_data in phases_data:
        department = departments.get(
            phase_data["department"]
        )

        if department is None:
            raise ValueError(
                "Required department not found: "
                f"{phase_data['department']}"
            )

        phase = WorkflowPhase.query.filter_by(
            slug=phase_data["slug"]
        ).first()

        if phase is None:
            phase = WorkflowPhase(
                name=phase_data["name"],
                slug=phase_data["slug"],
                department=department,
                phase_order=phase_data["phase_order"],
                description=phase_data["description"],
                is_final_approval=(
                    phase_data["is_final_approval"]
                ),
                is_active=True,
            )

            db.session.add(phase)

        else:
            phase.name = phase_data["name"]
            phase.department = department
            phase.phase_order = phase_data["phase_order"]
            phase.description = phase_data["description"]
            phase.is_final_approval = (
                phase_data["is_final_approval"]
            )
            phase.is_active = True


def seed_phase_checklist(
    *,
    phase_slug: str,
    checklist_items: list[dict],
) -> int:
    """
    Insert or update checklist items for a workflow phase.

    Existing items are matched using their phase and item text.

    Returns:
        Number of newly created checklist items.
    """

    phase = WorkflowPhase.query.filter_by(
        slug=phase_slug
    ).first()

    if phase is None:
        raise ValueError(
            f"Workflow phase not found: {phase_slug}"
        )

    created_count = 0

    for item_data in checklist_items:
        checklist_item = ChecklistItem.query.filter_by(
            phase_id=phase.id,
            item_text=item_data["item_text"],
        ).first()

        if checklist_item is None:
            checklist_item = ChecklistItem(
                phase=phase,
                section=item_data["section"],
                item_text=item_data["item_text"],
                display_order=item_data["display_order"],
                is_required=True,
                is_active=True,
            )

            db.session.add(checklist_item)
            created_count += 1

        else:
            checklist_item.section = item_data["section"]
            checklist_item.display_order = (
                item_data["display_order"]
            )
            checklist_item.is_required = True
            checklist_item.is_active = True

    return created_count


def seed_noc_checklist_items() -> int:
    """Seed the NOC access and security checklist."""

    noc_items = [
        {
            "section": "Identity & Access Management",
            "item_text": (
                "Active Directory / Domain Account disabled "
                "or access blocked."
            ),
            "display_order": 1,
        },
        {
            "section": "Identity & Access Management",
            "item_text": (
                "Corporate email account suspended and active "
                "sessions removed."
            ),
            "display_order": 2,
        },
        {
            "section": "Identity & Access Management",
            "item_text": (
                "VPN and remote access profiles revoked."
            ),
            "display_order": 3,
        },
        {
            "section": "Identity & Access Management",
            "item_text": (
                "Server, panel, cloud, SSH, or infrastructure "
                "access removed where applicable."
            ),
            "display_order": 4,
        },
        {
            "section": (
                "Communication Platforms & Security Groups"
            ),
            "item_text": (
                "Employee removed from official communication "
                "channels and groups."
            ),
            "display_order": 5,
        },
        {
            "section": (
                "Communication Platforms & Security Groups"
            ),
            "item_text": (
                "Firewall authentication, web proxy profile, "
                "and internet access rules removed or disabled."
            ),
            "display_order": 6,
        },
        {
            "section": (
                "Communication Platforms & Security Groups"
            ),
            "item_text": (
                "Endpoint security or mobile device management "
                "association removed where applicable."
            ),
            "display_order": 7,
        },
        {
            "section": (
                "Communication Platforms & Security Groups"
            ),
            "item_text": (
                "Shared account passwords changed where the "
                "employee had access."
            ),
            "display_order": 8,
        },
    ]

    return seed_phase_checklist(
        phase_slug="noc-access-security-clearance",
        checklist_items=noc_items,
    )


def seed_mis_checklist_items() -> int:
    """Seed the MIS business applications checklist."""

    mis_items = [
        {
            "section": "Business Applications Access",
            "item_text": (
                "SAP / ERP System access has been blocked "
                "or confirmed as not applicable."
            ),
            "display_order": 1,
        },
        {
            "section": "Business Applications Access",
            "item_text": (
                "PMS / Payroll Management System access has "
                "been blocked or confirmed as not applicable."
            ),
            "display_order": 2,
        },
        {
            "section": "Business Applications Access",
            "item_text": (
                "DMS / Document Management System access has "
                "been blocked or confirmed as not applicable."
            ),
            "display_order": 3,
        },
        {
            "section": "Business Applications Access",
            "item_text": (
                "Attendance / Biometric System access has been "
                "blocked or confirmed as not applicable."
            ),
            "display_order": 4,
        },
        {
            "section": "Business Applications Access",
            "item_text": (
                "CRM / Sales Portal access has been blocked "
                "or confirmed as not applicable."
            ),
            "display_order": 5,
        },
        {
            "section": "Business Applications Access",
            "item_text": (
                "SDMS / Sales and Distribution System access "
                "has been blocked or confirmed as not applicable."
            ),
            "display_order": 6,
        },
        {
            "section": "Business Applications Access",
            "item_text": (
                "Access to internal databases has been blocked "
                "or confirmed as not applicable."
            ),
            "display_order": 7,
        },
    ]

    return seed_phase_checklist(
        phase_slug="mis-business-applications-clearance",
        checklist_items=mis_items,
    )


def seed_hardware_checklist_items() -> int:
    """Seed the Hardware and Asset Recovery checklist."""

    hardware_items = [
        {
            "section": "Hardware and Asset Recovery",
            "item_text": (
                "The official laptop or desktop has been "
                "recovered, and its model and serial number "
                "have been recorded."
            ),
            "display_order": 1,
        },
        {
            "section": "Hardware and Asset Recovery",
            "item_text": (
                "Power adapters and peripherals, including "
                "chargers, mouse devices, keyboards, docking "
                "stations, and monitors, have been recovered."
            ),
            "display_order": 2,
        },
        {
            "section": "Hardware and Asset Recovery",
            "item_text": (
                "Storage media and security tokens, including "
                "external hard drives, encrypted USB drives, "
                "and OTP hardware, have been recovered."
            ),
            "display_order": 3,
        },
        {
            "section": "Hardware and Asset Recovery",
            "item_text": (
                "The company mobile handset and SIM card have "
                "been recovered, and any required carrier "
                "redirection has been requested."
            ),
            "display_order": 4,
        },
        {
            "section": "Hardware and Asset Recovery",
            "item_text": (
                "Physical access keys and cards, including "
                "facility keys, cabinet keys, RFID cards, and "
                "biometric smart cards, have been recovered."
            ),
            "display_order": 5,
        },
    ]

    return seed_phase_checklist(
        phase_slug="hardware-asset-recovery",
        checklist_items=hardware_items,
    )