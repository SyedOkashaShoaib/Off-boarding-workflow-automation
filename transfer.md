6. WORKFLOW PROCESSING MECHANISM

6.1 Case Initialization

NOC submits the new offboarding case form.

Flask-WTF validates the submitted fields and CSRF token.

The selected employee department is verified against the active department records.

A new OffboardingCase record is created.

The workflow phases are retrieved in their configured sequence.

The first WorkflowTask is activated and assigned a due date.

A secure task-access link and notification record are created.

The case initialization is recorded in the audit history.


6.2 Departmental Checklist Submission

The departmental user opens the secure task link received by email.

The system validates the access token, expiry time, and task status.

The checklist configured for the current workflow phase is displayed.

Each response and responsible departmental employee is validated.

A reason is required when Not Applicable is selected.

Valid responses are stored as ChecklistResponse records.

The current task is marked as completed.

The workflow progression process is then started.


6.3 Workflow Progression

Workflow tasks follow the sequence defined by the configured phases.

Only the current departmental task is available for completion.

Completion of the current task activates the next workflow phase.

A new secure link is generated for the next department.

The next assignment notification is created and sent.

After the last departmental task, the case moves to final approval.


> [INFO] Workflow phases, checklist items, departments, and departmental employees must be configured before cases are processed.



6.4 Final Approval and Closure

The final approver opens the completed case through the staff portal.

The system confirms that all required departmental tasks are complete.

The approver reviews the submitted checklist responses.

An approval or rejection decision is recorded.

Approval changes the case status to closed.

The decision and completion time are recorded in the audit history.

A rejected case remains available for further action according to the implemented workflow.



---

7. SECURE TASK-LINK MECHANISM

7.1 Link Generation

A secure random token is generated when a departmental task becomes active.

The raw token is included in the task URL sent to the department.

Only a SHA-256 digest of the token is stored in the database.

The access grant is linked to a specific workflow task.

An expiry time is assigned according to the configured token lifetime.


7.2 Link Validation

When the task URL is opened, the system:

extracts the token from the request;

calculates its SHA-256 digest;

searches for the corresponding TaskAccessGrant;

verifies that the grant has not expired;

checks that it has not been revoked;

confirms that the associated task is still available;

allows access only when all checks succeed.


Invalid, expired, or revoked links are rejected and do not expose the departmental checklist.

7.3 Link Reissue

NOC may reissue a task link when the original link is lost, expired, or considered compromised.

Existing active grants for the task are revoked.

A new token and access grant are generated.

A replacement notification is sent to the configured department address.

The reissue action is recorded for audit purposes.


> [SECURITY NOTE] The raw access token is not stored in the database and should not be displayed in logs, screenshots, or support documentation.




---

8. EMAIL NOTIFICATION SYSTEM

8.1 How Notifications Are Sent

A notification record is created when a workflow task becomes active.

The application prepares the relevant email content.

A secure task link is included where departmental action is required.

Delivery is attempted through the configured SMTP backend.

The notification status is updated after the attempt.

Delivery errors are stored for troubleshooting.

Console mode may be used during local development instead of sending an external email.


8.2 Notification Types

Notification	Purpose

Task assignment	Informs a department that its checklist is ready
Next-phase assignment	Notifies the next department after workflow progression
Replacement-link notification	Sends a newly issued secure task link
Overdue escalation	Informs NOC that a task has passed its due date
Final-approval notification	Indicates that the case is ready for final review


8.3 Departmental Email Contents

A departmental assignment email normally includes:

case reference;

assigned department or workflow phase;

employee information required for identification;

task due date;

secure task link;

brief completion instructions.


8.4 Notification Tracking

Status	Meaning

Pending	Notification has been created but delivery is not yet confirmed
Sent	SMTP delivery completed successfully
Failed	Delivery was unsuccessful and an error was recorded


> [NOTE] A failed email does not necessarily mean that the case or workflow task was not created. The case record, active task, access grant, and notification status should be checked separately.




---

9. SECURITY IMPLEMENTATION

9.1 Implemented Security Controls

Security Control	Implementation

Staff authentication	Flask-Login with email and password authentication
Password protection	Passwords stored as secure hashes rather than plaintext
Role-based authorization	Protected portal routes restricted by operational role
Departmental access	Task-specific secure URLs instead of general portal access
Token protection	Only SHA-256 token digests stored in the database
Token expiry	Configurable expiry time for task-access links
Token revocation	Existing grants can be invalidated during link reissue
CSRF protection	Flask-WTF CSRF validation on state-changing forms
Session protection	HTTP-only and SameSite cookie configuration
Audit logging	Important case, access, workflow, and approval actions recorded
Input validation	Form and server-side validation applied before database changes


9.2 Access Boundaries

NOC users access case creation, monitoring, and operational controls through the staff portal.

Departmental users access only the task associated with their secure link.

The final approver accesses completed cases requiring a decision.

Unauthorized users are prevented from accessing protected routes or unrelated departmental tasks.


9.3 Current Security Limitations

Limitation	Required Production Action

Prototype deployment environment	Complete infrastructure and security review
Local SQLite database	Select and secure an approved production database
No Active Directory or SSO integration	Evaluate organizational authentication integration
Development server	Deploy through an approved production WSGI server
No formal penetration test	Perform security testing before production release
Environment-based secrets	Use approved secret-management and server controls
HTTPS dependent on deployment	Configure TLS certificates and secure cookies in production


> [WARNING] The application should not be described as production-secure until deployment architecture, HTTPS, backups, monitoring, access policies, and formal security testing have been completed.