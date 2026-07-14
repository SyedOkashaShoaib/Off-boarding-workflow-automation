import click
from flask.cli import with_appcontext

from app.extension import db
from app.models import Department, WorkflowPhase, ChecklistItem


def seed_phase_checklist(
        phase: WorkflowPhase,
        section: str,
        item_texts: list[str],
)->int:
    created_count = 0
    for display_order, item_text in enumerate(
        item_texts,
        start=1,
    ):
        existing_item = (
            ChecklistItem.query
            .filter_by(
                phase_id=phase.id,
                item_text=item_text,
            )
            .first()
        )
        if existing_item is None: 
            existing_item=ChecklistItem(
                phase=phase,
                section=section,
                item_text=item_text,
                display_order=display_order,
                is_required=True,
                is_active=True,
            )
            db.session.add(existing_item)
            created_count+=1
        else:
            existing_item.section=section
            existing_item.display_order=display_order
            existing_item.is_required = True
            existing_item.is_active=True

    return created_count


@click.command("seed-data")
@with_appcontext
def seed_data_command():
    seed_departments()
    seed_workflow_phases()
    
    seed_noc_checklist_items()

    db.session.commit()
    click.echo("Seed data inserted successfully.")


def seed_departments():
    departments_data = [
        {
            "name": "NOC",
            "email": "internee@company.com"
        },
        {
            "name": "MIS",
            "email": "internee@company.com"
        },
        {
            "name": "Hardware",
            "email": "internee@company.com"
        },
        {
            "name": "Admin",
            "email": "internee@company.com"
        },
    ]

    for dept_data in departments_data:
        department = Department.query.filter_by(name=dept_data["name"]).first()

        if department is None:
            department = Department(
                name=dept_data["name"],
                email=dept_data["email"],
                is_active=True
            )
            db.session.add(department)
        else:
            department.email = dept_data["email"]
            department.is_active = True


def seed_workflow_phases():
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
            "description": "Merged NOC phase covering identity, access, communication, and security clearance.",
            "is_final_approval": False,
        },
        {
            "name": "MIS Business Applications Clearance",
            "slug": "mis-business-applications-clearance",
            "department": "MIS",
            "phase_order": 2,
            "description": "Clearance of business applications, internal systems, and software access.",
            "is_final_approval": False,
        },
        {
            "name": "Hardware & Asset Recovery",
            "slug": "hardware-asset-recovery",
            "department": "Hardware",
            "phase_order": 3,
            "description": "Recovery of company hardware, accessories, and assigned physical assets.",
            "is_final_approval": False,
        },
        {
            "name": "Admin Final Approval",
            "slug": "admin-final-approval",
            "department": "Admin",
            "phase_order": 4,
            "description": "Final administrative approval before closing the offboarding case.",
            "is_final_approval": True,
        },
    ]

    for phase_data in phases_data:
        department = departments.get(phase_data["department"])

        if department is None:
            raise ValueError(f"Department not found: {phase_data['department']}")

        phase = WorkflowPhase.query.filter_by(slug=phase_data["slug"]).first()

        if phase is None:
            phase = WorkflowPhase(
                name=phase_data["name"],
                slug=phase_data["slug"],
                department_id=department.id,
                phase_order=phase_data["phase_order"],
                description=phase_data["description"],
                is_final_approval=phase_data["is_final_approval"],
                is_active=True
            )
            db.session.add(phase)
        else:
            phase.name = phase_data["name"]
            phase.department_id = department.id
            phase.phase_order = phase_data["phase_order"]
            phase.description = phase_data["description"]
            phase.is_final_approval = phase_data["is_final_approval"]
            phase.is_active = True


def seed_noc_checklist_items():
    noc_phase = WorkflowPhase.query.filter_by(
        slug="noc-access-security-clearance"
    ).first()

    if noc_phase is None:
        raise ValueError("NOC workflow phase not found. Seed workflow phases first.")

    noc_items = [
        {
            "section": "Identity & Access Management",
            "item_text": "Active Directory / Domain Account disabled or access blocked.",
            "display_order": 1,
        },
        {
            "section": "Identity & Access Management",
            "item_text": "Corporate email account suspended and active sessions removed.",
            "display_order": 2,
        },
        {
            "section": "Identity & Access Management",
            "item_text": "VPN and remote access profiles revoked.",
            "display_order": 3,
        },
        {
            "section": "Identity & Access Management",
            "item_text": "Server, panel, cloud, SSH, or infrastructure access removed where applicable.",
            "display_order": 4,
        },
        {
            "section": "Communication Platforms & Security Groups",
            "item_text": "Employee removed from official communication channels and groups.",
            "display_order": 5,
        },
        {
            "section": "Communication Platforms & Security Groups",
            "item_text": "Firewall authentication, web proxy profile, and internet access rules removed or disabled.",
            "display_order": 6,
        },
        {
            "section": "Communication Platforms & Security Groups",
            "item_text": "Endpoint security or mobile device management association removed where applicable.",
            "display_order": 7,
        },
        {
            "section": "Communication Platforms & Security Groups",
            "item_text": "Shared account passwords changed where the employee had access.",
            "display_order": 8,
        },
    ]

    for item_data in noc_items:
        checklist_item = ChecklistItem.query.filter_by(
            phase_id=noc_phase.id,
            item_text=item_data["item_text"]
        ).first()

        if checklist_item is None:
            checklist_item = ChecklistItem(
                phase_id=noc_phase.id,
                section=item_data["section"],
                item_text=item_data["item_text"],
                display_order=item_data["display_order"],
                is_required=True,
                is_active=True
            )
            db.session.add(checklist_item)
        else:
            checklist_item.section = item_data["section"]
            checklist_item.display_order = item_data["display_order"]
            checklist_item.is_required = True
            checklist_item.is_active = True