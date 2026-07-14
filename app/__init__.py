from flask import Flask
from config import Config
from app.extension import db, migrate
from app.overdue_commands import process_overdue_tasks_command
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    from app import models  
    from app.routes.case_routes import case_bp
    from app.routes.main_routes import main_bp
    from app.routes.workflow_routes import workflow_bp
    app.register_blueprint(case_bp, url_prefix='/cases')
    app.register_blueprint(main_bp) 
    app.register_blueprint(workflow_bp)

    from app.commands import seed_data_command
    app.cli.add_command(seed_data_command)
    app.cli.add_command(process_overdue_tasks_command)
    return app