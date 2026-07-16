from typing import Optional

from flask import Flask

from config import Config

from app.extension import (
    db,
    login_manager,
    migrate,
)
from app.overdue_commands import (
    process_overdue_tasks_command,
)


def create_app() -> Flask:
    """
    Create and configure the Flask application.
    """

    app = Flask(__name__)
    app.config.from_object(Config)

    # --------------------------------------------------------
    # Flask extensions
    # --------------------------------------------------------

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    login_manager.login_view = "auth.login"
    login_manager.login_message = (
        "Sign in to access the offboarding operations portal."
    )
    login_manager.login_message_category = "warning"
    login_manager.session_protection = "strong"

    # Import models after extension initialization so SQLAlchemy
    # metadata contains all mapped database tables.
    from app import models
    from app.models import User

    @login_manager.user_loader
    def load_user(
        user_id: str,
    ) -> Optional[User]:
        """
        Reload the authenticated user from the session identifier.
        """

        try:
            parsed_user_id = int(user_id)
        except (TypeError, ValueError):
            return None

        if parsed_user_id < 1:
            return None

        return db.session.get(
            User,
            parsed_user_id,
        )

    # --------------------------------------------------------
    # Blueprints
    # --------------------------------------------------------

    from app.routes.case_routes import case_bp
    from app.routes.main_routes import main_bp
    from app.routes.workflow_routes import workflow_bp

    app.register_blueprint(
        case_bp,
        url_prefix="/cases",
    )

    app.register_blueprint(main_bp)
    app.register_blueprint(workflow_bp)

    # --------------------------------------------------------
    # CLI commands
    # --------------------------------------------------------

    from app.auth_commands import (
        create_portal_user_command,
    )
    from app.commands import seed_data_command

    app.cli.add_command(seed_data_command)
    app.cli.add_command(
        process_overdue_tasks_command
    )
    app.cli.add_command(
        create_portal_user_command
    )

    return app