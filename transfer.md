10.3 Entity Descriptions

10.3.1 User

The User entity stores accounts permitted to access the authenticated operations portal. Each user is identified by a unique email address and has a stored password hash, full name, authorization role, active status, login timestamp, and record timestamps. Supported roles include NOC_OPERATOR, FINAL_APPROVER, and SYSTEM_ADMIN. Passwords are stored as hashes rather than plaintext values. The entity does not contain foreign keys to other database tables because portal authorization is role-based rather than directly linked to workflow departments.

10.3.2 Department

The Department entity represents departments that participate in the offboarding clearance workflow, such as NOC, MIS, Hardware, and Administration. Each department has a unique name, an email address used for workflow assignment and notification, and an active-status field. One department may contain multiple department employees and may be responsible for multiple workflow phases.

10.3.3 DepartmentEmployee

The DepartmentEmployee entity stores employees who may be selected as responsible for individual checklist responses. Each record belongs to one workflow department through department_id and contains a unique employee code, full name, and active status. The entity is connected to ChecklistResponse, allowing the system to record the specific departmental employee responsible for each clearance item.

10.3.4 WorkflowPhase

The WorkflowPhase entity defines the ordered stages through which an offboarding case progresses. Each phase belongs to one department and includes a name, unique slug, sequence number, optional description, active status, and an indicator specifying whether the phase represents final approval. A workflow phase may contain multiple checklist items and may be referenced by multiple workflow tasks.

10.3.5 ChecklistItem

The ChecklistItem entity defines an individual clearance requirement belonging to a workflow phase. Each checklist item contains the requirement text, an optional section heading, display order, required-status indicator, and active-status indicator. The phase_id foreign key determines the workflow phase in which the item appears. One checklist item may be referenced by multiple checklist responses across different offboarding cases.

10.3.6 EmployeeDepartment

The EmployeeDepartment entity stores the organizational departments of employees being offboarded, such as Finance, Sales, Human Resources, or Manufacturing. It is separate from the Department entity because it represents the employee’s home department rather than a department responsible for performing workflow clearance. Each name is unique and may be deactivated through the is_active field. The table does not have a foreign-key relationship with OffboardingCase; the selected department name is stored in the case as text.

10.3.7 OffboardingCase

The OffboardingCase entity is the central operational record in the database. It stores the case number, employee information, designation, organizational department, final working date, line manager, case status, creator, timestamps, and current workflow phase. The case_number field is unique, while current_phase_id references the phase currently responsible for processing the case.

One offboarding case may contain multiple workflow tasks and audit-log records. The case also maintains created_at, updated_at, and closed_at timestamps to support lifecycle tracking.

10.3.8 WorkflowTask

The WorkflowTask entity represents the execution of one workflow phase for one offboarding case. Each task belongs to an OffboardingCase and a WorkflowPhase through the case_id and phase_id foreign keys. It records the assigned email address, task status, assignment time, due time, opening time, and submission time.

A unique constraint on case_id and phase_id ensures that the same workflow phase cannot generate more than one task for a particular case. One workflow task may contain multiple checklist responses, task-access grants, and email notifications.

10.3.9 ChecklistResponse

The ChecklistResponse entity stores the submitted result for one checklist item within a workflow task. Each response references an offboarding case, workflow task, checklist item, and responsible department employee. It also records the response status, optional reason, submitting identity, and submission timestamp.

A unique constraint on workflow_task_id and checklist_item_id prevents the same checklist item from receiving more than one stored response within the same task.

10.3.10 TaskAccessGrant

The TaskAccessGrant entity supports secure, task-specific access for departments that do not use permanent portal accounts. Each grant belongs to one workflow task and records the SHA-256 hash of the access token, intended recipient email, expiration time, creation time, access count, most recent access time, consumption time, and revocation time.

The raw token sent through email is not stored in the database. The token_hash field is unique, and multiple historical grants may exist for one task when links are replaced, revoked, or consumed.

10.3.11 AuditLog

The AuditLog entity stores a chronological history of significant actions associated with an offboarding case. Each record references one case and contains an action identifier, the responsible actor, optional event details, and the event timestamp. Examples of recorded events include task creation, task opening, checklist submission, secure-link activation, notification delivery, final approval, and case closure.

An index on case_id and created_at supports efficient retrieval of a case’s audit history in chronological order.

10.3.12 EmailNotification

The EmailNotification entity records emails created and delivered during the workflow. Each notification is associated with both an offboarding case and a workflow task. It records the notification category, recipient email, subject, delivery status, optional deduplication key, provider message identifier, error details, creation time, attempt time, and successful sending time.

The entity supports assignment emails, replacement secure-link emails, and overdue escalation messages. Its indexes support queries by case and delivery status, as well as by workflow task and notification type.

The next section is 10.4 Relationship Summary, which converts the ERD relationships into a concise written explanation.