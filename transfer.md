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
            "full_name": "NOC Officer 1",
            "department": "NOC",
        },
        {
            "employee_code": "NOC-002",
            "full_name": "NOC Officer 2",
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