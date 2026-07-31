Yes. The folder structure should be documented before installation instructions because it helps another developer understand where configuration, routes, services, templates, and database files are located.

Rename the next sections as follows:

12.1 Current Development Environment
12.2 Project Directory Structure
12.3 Application Installation and Setup
12.4 Database Initialization

12.2 Project Directory Structure

The source code is divided into folders according to operational responsibility. Route handlers, form definitions, business services, database models, interface templates, static assets, configuration, and migration files are maintained separately. This structure makes it easier to locate and modify a particular part of the system without placing all application logic in one file.

The principal project structure is shown below. Individual template, stylesheet, JavaScript, and migration files may be omitted from the diagram where only their containing folder is relevant.

Off-boarding-workflow-automation/
│
├── app/
│   ├── __init__.py
│   ├── extension.py
│   ├── models.py
│   ├── commands.py
│   ├── auth_commands.py
│   ├── overdue_commands.py
│   │
│   ├── routes/
│   │   ├── main_routes.py
│   │   ├── auth_routes.py
│   │   ├── case_routes.py
│   │   ├── workflow_routes.py
│   │   └── task_access_route.py
│   │
│   ├── forms/
│   │   ├── auth_forms.py
│   │   ├── offboarding_case.py
│   │   ├── workflow_forms.py
│   │   └── case_action_forms.py
│   │
│   ├── services/
│   │   ├── workflow_service.py
│   │   ├── checklist_service.py
│   │   ├── approval_service.py
│   │   ├── case_query_service.py
│   │   ├── task_access_service.py
│   │   ├── task_access_reissue_service.py
│   │   ├── notification_service.py
│   │   └── email_service.py
│   │
│   ├── templates/
│   │   ├── base.html
│   │   ├── layouts/
│   │   ├── cases/
│   │   └── workflow/
│   │
│   └── static/
│       ├── css/
│       │   ├── app.css
│       │   └── pages/
│       └── js/
│
├── migrations/
│   ├── versions/
│   ├── env.py
│   └── script.py.mako
│
├── config.py
├── run.py
├── requirements.txt
├── .gitignore
└── README.md

12.2.1 Application Package

The app directory contains the main application source code. It is implemented as a Python package and contains the database models, route handlers, forms, service modules, templates, static files, and command-line utilities.

app/__init__.py

The app/__init__.py file contains the application-factory function, create_app(). It creates the Flask application, loads the configuration, initializes the database, migration and login extensions, registers the application blueprints, and attaches the custom Flask command-line commands.

The following route blueprints are registered by the application factory:

case_bp
auth_bp
main_bp
workflow_bp
task_access_bp

The case blueprint is registered with the /cases URL prefix, while the remaining blueprints define their route prefixes internally.

The application factory also registers commands for:

seed-data
process-overdue-tasks
create-portal-user

These commands support reference-data initialization, overdue-task processing, and portal-user administration.

app/extension.py

The extension.py file defines shared Flask extension objects, including the SQLAlchemy database object, Flask-Migrate integration, and Flask-Login manager.

These objects are defined separately from the application factory so they can be imported by models, routes, and services without creating circular imports. The objects are connected to the Flask application during execution of create_app().

app/models.py

The models.py file defines the SQLAlchemy model classes corresponding to the application’s database tables.

It contains the entities documented in Chapter 10, including:

User
Department
DepartmentEmployee
WorkflowPhase
ChecklistItem
EmployeeDepartment
OffboardingCase
WorkflowTask
ChecklistResponse
TaskAccessGrant
AuditLog
EmailNotification

Database columns, relationships, indexes, unique constraints, validation methods, and model-level utility functions are maintained in this file.

12.2.2 Routes Directory

The app/routes directory contains the HTTP route handlers. Routes receive browser requests, enforce the required access rules, process form submissions, call the relevant service functions, and return rendered templates or redirects.

The current route modules are:

Route module	Responsibility

main_routes.py	Handles the application’s root and general navigation routes
auth_routes.py	Handles portal login, logout, and authenticated-session operations
case_routes.py	Handles case creation, case listing, case details, and case-level actions
workflow_routes.py	Handles departmental checklist tasks, task submission, and final approval
task_access_route.py	Handles activation and validation of secure task-access links


The route modules should remain responsible for request handling rather than containing extensive business logic. Workflow processing, notification creation, access-grant management, and checklist persistence are delegated to service modules.

12.2.3 Forms Directory

The app/forms directory contains Flask-WTF form classes and field-validation rules. Separating forms from route modules prevents request-validation code from becoming mixed with workflow processing logic.

The current form modules are:

Form module	Responsibility

auth_forms.py	Login, logout, and authentication-related forms
offboarding_case.py	Employee offboarding case-creation form
workflow_forms.py	Departmental checklist and workflow-submission forms
case_action_forms.py	Case-level operational actions, including access-link reissue actions


These forms provide server-side input validation and integrate Flask-WTF’s CSRF protection into state-changing requests.

12.2.4 Services Directory

The app/services directory contains the system’s business and workflow-processing logic. Service functions are called by route handlers and command-line commands.

The principal service modules include:

Service module	Responsibility

workflow_service.py	Creates workflow tasks and advances cases between phases
checklist_service.py	Validates and stores departmental checklist responses
approval_service.py	Processes final approval and case closure
case_query_service.py	Retrieves and filters cases for operational views
task_access_service.py	Creates, validates, consumes, and revokes secure task-access grants
task_access_reissue_service.py	Reissues task links and handles replacement-link operations
notification_service.py	Creates and manages workflow notification records
email_service.py	Sends or displays email messages through the configured backend


These modules are present separately from the routes so that the same workflow operations can be invoked from different interfaces without duplicating logic. For example, notification processing may be initiated by a browser route or by an overdue-task command.

12.2.5 Command Modules

The application contains three command-related modules:

commands.py

This file contains the data-seeding command used to create the initial workflow departments, phases, checklist items, department employees, and employee-department lookup records required by the application.

auth_commands.py

This file contains the command used to create authenticated portal accounts. Portal-user creation is performed through a controlled command rather than through a publicly accessible registration page.

overdue_commands.py

This file contains the process-overdue-tasks command. It identifies overdue workflow tasks and creates or retries the corresponding overdue notifications.

The command is registered with Flask by the application factory.

12.2.6 Templates Directory

The app/templates directory contains Jinja templates used to generate the HTML interface.

The templates are grouped by interface purpose:

templates/
├── base.html
├── layouts/
├── cases/
└── workflow/

base.html provides the main authenticated application shell and references the shared static/css/app.css stylesheet.

The layouts directory contains alternative base layouts for interfaces that do not use the complete operations-portal shell, including the authentication interface and secure departmental task interface.

The cases directory contains templates for case listing, case details, and case-level actions. The workflow directory contains templates for departmental tasks and final approval.

12.2.7 Static Directory

The app/static directory contains browser-delivered interface assets, principally CSS stylesheets and JavaScript files.

The shared application stylesheet is located at:

app/static/css/app.css

Page-specific stylesheets are stored separately under static/css/pages. For example, the case-listing template loads:

static/css/pages/cases.css

Keeping page-specific styling separate from the shared application stylesheet reduces the risk of unrelated pages being affected by localized interface changes.

JavaScript files support client-side interactions such as filtering, conditional form controls, and task-interface behaviour. Core validation and authorization must nevertheless remain server-side because browser-side controls can be bypassed.

12.2.8 Migrations Directory

The migrations directory contains the Alembic migration environment and the recorded history of database schema changes.

migrations/
├── versions/
├── env.py
└── script.py.mako

The versions directory contains individual migration scripts for operations such as:

creating initial tables;

adding email notifications;

adding secure task-access grants;

creating the portal-user table;

adding database indexes;

adding notification deduplication;

adding the department-employee directory;

updating checklist-response accountability.


Migration files should be retained in version control because they provide the ordered instructions required to recreate or upgrade the database schema.

12.2.9 Root-Level Files

File	Purpose

config.py	Reads environment variables and defines application configuration
run.py	Creates and starts the Flask application locally
requirements.txt	Records the Python dependencies and pinned versions
.gitignore	Excludes secrets, databases, environments, caches, and local editor files
README.md	Provides the repository’s introductory project information


The run.py entry point imports create_app(), constructs the application instance, and starts the development server.

12.2.10 Separation of Responsibilities

The directory structure follows the following operational separation:

Routes       → receive and respond to HTTP requests
Forms        → define and validate submitted input
Services     → execute workflow and business rules
Models       → store and relate persistent data
Templates    → generate the browser interface
Static files → provide styling and browser-side behaviour
Commands     → perform administrative and scheduled operations
Migrations   → maintain database schema history
Configuration→ supply environment-specific settings

This section should explain where the code is located, rather than repeating the detailed system architecture or the complete behaviour of each workflow component.

The next section is 12.3 Application Installation and Setup.