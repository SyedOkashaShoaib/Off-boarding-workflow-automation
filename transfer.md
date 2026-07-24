(.venv) PS C:\Users\intern\Desktop\intern_summer_26\offboarding_workflow> git checkout --ours -- .
(.venv) PS C:\Users\intern\Desktop\intern_summer_26\offboarding_workflow> git add -A
(.venv) PS C:\Users\intern\Desktop\intern_summer_26\offboarding_workflow> git diff --name-only --diff-filter=U
(.venv) PS C:\Users\intern\Desktop\intern_summer_26\offboarding_workflow> git grep -n -E "^(<<<<<<<|=======|>>>>>>>)"
(.venv) PS C:\Users\intern\Desktop\intern_summer_26\offboarding_workflow> git diff --stat ORIG_HEAD
 app/__init__.py                                    |   96 +-
 app/auth_commands.py                               |  123 --
 app/extension.py                                   |    5 +-
 app/forms/auth_forms.py                            |   74 --
 app/forms/offboarding_case.py                      |    8 +-
 app/forms/workflow_forms.py                        |   57 -
 app/routes/auth_routes.py                          |  229 ----
 app/routes/main_routes.py                          |   29 +-
 app/routes/task_access_route.py                    |  196 ---
 app/services/approval_service.py                   |  171 ---
 app/services/case_query_service.py                 | 1021 ---------------
 app/services/overdue_service.py                    |  135 --
 app/services/task_access_service.py                |  585 ---------
 app/services/workflow_service.py                   |  238 +---
 app/static/css/app.css                             | 1299 --------------------
 app/static/css/pages/auth.css                      |  203 ---
 app/static/css/pages/task_access.css               |  105 --
 app/static/css/style.css                           |    0
 app/templates/auth/login.html                      |  118 --
 app/templates/base.html                            |  375 +-----
 app/templates/case_created.html                    |  187 +--
 app/templates/dashboard.html                       |    0
 app/templates/layouts/auth_base.html               |  142 ---
 app/templates/layouts/task_base.html               |  108 --
 app/templates/task_access/continue.html            |  124 --
 app/templates/task_access/unavailable.html         |   32 -
 app/templates/workflow/admin_approval.html         |  273 ----
 .../versions/066ccd71be93_auth_portal_users.py     |   45 -
 .../0d2eb512e3b1_added_emailnotification_class.py  |   42 -
 ...ace7b106cf_add_secure_dep_task_access_grants.py |   48 -
 .../versions/6e49f821eca5_correct_index_name.py    |   34 -
 migrations/versions/72ca45eb4245_add_indexes.py    |   58 -
 ...ff896573a_fixed_version_bug_and_added_email_.py |   60 -
 .../b8c3e036fdd3_add_deduplication_key_column.py   |   34 -
 35 files changed, 76 insertions(+), 6406 deletions(-)
(.venv) PS C:\Users\intern\Desktop\intern_summer_26\offboarding_workflow> git diff ORIG_HEAD
diff --git a/app/__init__.py b/app/__init__.py
index e703362..3e94b98 100644
--- a/app/__init__.py
+++ b/app/__init__.py
@@ -1,106 +1,20 @@
-from typing import Optional
-
 from flask import Flask
-
 from config import Config
+from app.extension import db, migrate

-from app.extension import (
-    db,
-    login_manager,
-    migrate,
-)
-from app.overdue_commands import (
-    process_overdue_tasks_command,
-)
-
-
-def create_app() -> Flask:
-    """
-    Create and configure the Flask application.
-    """
-
+def create_app():
     app = Flask(__name__)
     app.config.from_object(Config)

-    # --------------------------------------------------------
-    # Flask extensions
-    # --------------------------------------------------------
-
     db.init_app(app)
     migrate.init_app(app, db)
-    login_manager.init_app(app)
-
-    login_manager.login_view = "auth.login"
-    login_manager.login_message = (
-        "Sign in to access the offboarding operations portal."
-    )
-    login_manager.login_message_category = "warning"
-    login_manager.session_protection = "strong"
-
-    # Import models after extension initialization so SQLAlchemy
-    # metadata contains all mapped database tables.
-    from app import models
-    from app.models import User
-
-    @login_manager.user_loader
-    def load_user(
-        user_id: str,
-    ) -> Optional[User]:
-        """
-        Reload the authenticated user from the session identifier.
-        """
-
-        try:
-            parsed_user_id = int(user_id)
-        except (TypeError, ValueError):
-            return None
-
-        if parsed_user_id < 1:
-            return None
-
-        return db.session.get(
-            User,
-            parsed_user_id,
-        )
-
-    # --------------------------------------------------------
-    # Blueprints
-    # --------------------------------------------------------

+    from app import models  
     from app.routes.case_routes import case_bp
     from app.routes.main_routes import main_bp
-    from app.routes.workflow_routes import workflow_bp
-    from app.routes.auth_routes import auth_bp
-    from app.routes.task_access_route import task_access_bp
-    app.register_blueprint(
-        case_bp,
-        url_prefix="/cases",
-    )
-    app.register_blueprint(auth_bp)
-    app.register_blueprint(main_bp)
-    app.register_blueprint(workflow_bp)
-    app.register_blueprint(task_access_bp)
-    # --------------------------------------------------------
-    # CLI commands
-    # --------------------------------------------------------
+    app.register_blueprint(case_bp, url_prefix='/cases')
+    app.register_blueprint(main_bp) 

-    from app.auth_commands import (
-        create_portal_user_command,
-    )
     from app.commands import seed_data_command
-
     app.cli.add_command(seed_data_command)
-    app.cli.add_command(
-        process_overdue_tasks_command
-    )
-    app.cli.add_command(
-        create_portal_user_command
-    )
-    from app.forms.auth_forms import LogoutForm
-
-    @app.context_processor
-    def inject_portal_forms():
-        return {
-            "logout_form":LogoutForm(),
-        }
     return app
\ No newline at end of file
diff --git a/app/auth_commands.py b/app/auth_commands.py
deleted file mode 100644
index 34190de..0000000
--- a/app/auth_commands.py
+++ /dev/null
@@ -1,123 +0,0 @@
-import click
-from flask.cli import with_appcontext
-from sqlalchemy.exc import SQLAlchemyError
-
-from app.extension import db
-from app.models import (
-    PORTAL_ROLES,
-    ROLE_NOC_OPERATOR,
-    User,
-)
-
-
-@click.command(
-    "create-portal-user"
-)
-@click.option(
-    "--email",
-    prompt="Email address",
-    help="Corporate email address used for portal login.",
-)
-@click.option(
-    "--full-name",
-    prompt="Full name",
-    help="User's display name.",
-)
-@click.option(
-    "--role",
-    type=click.Choice(
-        PORTAL_ROLES,
-        case_sensitive=False,
-    ),
-    default=ROLE_NOC_OPERATOR,
-    show_default=True,
-    help="Portal authorization role.",
-)
-@click.option(
-    "--password",
-    prompt=True,
-    hide_input=True,
-    confirmation_prompt=True,
-    help="Initial portal password.",
-)
-@with_appcontext
-def create_portal_user_command(
-    email: str,
-    full_name: str,
-    role: str,
-    password: str,
-) -> None:
-    """
-    Create an authenticated portal account.
-
-    There is deliberately no public user-registration page.
-    Portal accounts are provisioned through an administrative
-    process until corporate identity integration is implemented.
-    """
-
-    normalized_email = User.normalize_email(
-        email
-    )
-
-    normalized_full_name = str(
-        full_name or ""
-    ).strip()
-
-    normalized_role = str(
-        role or ""
-    ).strip().upper()
-
-    if not normalized_email:
-        raise click.ClickException(
-            "Email address is required."
-        )
-
-    if not normalized_full_name:
-        raise click.ClickException(
-            "Full name is required."
-        )
-
-    if len(password) < 3: #change this later on.... :)
-        raise click.ClickException(
-            "Password must contain at least 3 characters."
-        )
-
-    existing_user = (
-        User.query
-        .filter_by(
-            email=normalized_email
-        )
-        .first()
-    )
-
-    if existing_user is not None:
-        raise click.ClickException(
-            "A portal user with that email already exists."
-        )
-
-    user = User(
-        email=normalized_email,
-        full_name=normalized_full_name,
-        role=normalized_role,
-        active=True,
-    )
-
-    user.set_password(password)
-
-    try:
-        db.session.add(user)
-        db.session.commit()
-
-    except (SQLAlchemyError, ValueError) as exc:
-        db.session.rollback()
-
-        raise click.ClickException(
-            "The portal user could not be created."
-        ) from exc
-
-    click.echo(
-        (
-            "Portal user created successfully: "
-            f"{user.email} [{user.role}]"
-        )
-    )
\ No newline at end of file
diff --git a/app/extension.py b/app/extension.py
index f32307f..de1947d 100644
--- a/app/extension.py
+++ b/app/extension.py
@@ -1,6 +1,5 @@
 from flask_sqlalchemy import SQLAlchemy
-
-    try:
-        db.session.add(user)
-        db.session.commit()
-
-    except (SQLAlchemyError, ValueError) as exc:
-        db.session.rollback()
-
-        raise click.ClickException(
-            "The portal user could not be created."
-        ) from exc
-
-    click.echo(
-        (
-            "Portal user created successfully: "
-            f"{user.email} [{user.role}]"
-        )
-    )
\ No newline at end of file
diff --git a/app/extension.py b/app/extension.py
index f32307f..de1947d 100644
--- a/app/extension.py
+++ b/app/extension.py
@@ -1,6 +1,5 @@
 from flask_sqlalchemy import SQLAlchemy
-    user.set_password(password)

























-
-    user.set_password(password)
-
-    try:
-        db.session.add(user)
-        db.session.commit()
-
-    except (SQLAlchemyError, ValueError) as exc:
-        db.session.rollback()
-
-        raise click.ClickException(
-            "The portal user could not be created."







-        ) from exc
-
-    click.echo(   
-        (
-            "Portal user created successfully: "
-            f"{user.email} [{user.role}]"       
-        )
-    )
\ No newline at end of file
diff --git a/app/extension.py b/app/extension.py
index f32307f..de1947d 100644
--- a/app/extension.py
+++ b/app/extension.py
@@ -1,6 +1,5 @@
@@ -1,6 +1,5 @@

-    user.set_password(password)
-    user.set_password(password)
-
-    try:
-        db.session.add(user)
-        db.session.commit()
-
-    except (SQLAlchemyError, ValueError) as exc:
-        db.session.rollback()
-
-        raise click.ClickException(
-            "The portal user could not be created."
-        ) from exc
-
-    click.echo(
-        (
-            "Portal user created successfully: "
-            f"{user.email} [{user.role}]"
-        )
-    )
\ No newline at end of file
diff --git a/app/extension.py b/app/extension.py
index f32307f..de1947d 100644
--- a/app/extension.py
+++ b/app/extension.py
@@ -1,6 +1,5 @@
 from flask_sqlalchemy import SQLAlchemy
 from flask_migrate import Migrate
-from flask_login import LoginManager
+
 db = SQLAlchemy()
-migrate = Migrate()
-login_manager=LoginManager()
\ No newline at end of file
+migrate = Migrate()
\ No newline at end of file
diff --git a/app/forms/auth_forms.py b/app/forms/auth_forms.py
deleted file mode 100644
index 992ac8d..0000000
--- a/app/forms/auth_forms.py
+++ /dev/null
@@ -1,74 +0,0 @@
-from flask_wtf import FlaskForm
-from wtforms import (
-    HiddenField,
-    PasswordField,
-    StringField,
-    SubmitField,
-)
-from wtforms.validators import (
-    DataRequired,
-    Email,
-    Length,
-)
-
-
-class LoginForm(FlaskForm):
-    """
-    Portal login form.
-
-    The hidden next_url field preserves the protected page the user
-    originally requested. The route must validate it before redirecting.
-    """
-
-    email = StringField(
-        "Email Address",
-        validators=[
-            DataRequired(
-                message="Email address is required."
-            ),
-            Email(
-                message="Enter a valid email address."
-            ),
-            Length(
-                max=254,
-                message=(
-                    "Email address cannot exceed "
-                    "254 characters."
-                ),
-            ),
-        ],
-    )
-
-    password = PasswordField(
-        "Password",
-        validators=[
-            DataRequired(
-                message="Password is required."
-            ),
-            Length(
-                max=512,
-                message="Password is too long.",
-            ),
-        ],
-    )
-
-    next_url = HiddenField()
-
-    submit = SubmitField("Sign In")
-
-
-class LogoutForm(FlaskForm):
-    """
-    CSRF-protected logout request.
-    """
-
-    submit = SubmitField("Sign Out")
-
-class TaskAccessContinueForm(FlaskForm):
-    """
-    Confirm that a human user intends to open the assigned task.
-    """
-
-    submit = SubmitField(
-        "Open Assigned Task"
-    )
\ No newline at end of file
diff --git a/app/forms/offboarding_case.py b/app/forms/offboarding_case.py
index e050775..5a781e2 100644
--- a/app/forms/offboarding_case.py
+++ b/app/forms/offboarding_case.py
@@ -6,9 +6,9 @@ class Case_Form(FlaskForm):
     emp_name = StringField(label='Employee name', validators=[DataRequired(message="Employee name is required")] )
:
