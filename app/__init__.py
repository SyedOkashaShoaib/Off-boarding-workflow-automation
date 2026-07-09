from flask import Flask
from config import Config
from app.extension import db, migrate

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    from app import models  
    from app.routes.case_routes import case_bp
    from app.routes.main_routes import main_bp
    app.register_blueprint(case_bp, url_prefix='/cases')
    app.register_blueprint(main_bp) 

    # from app.commands import seed_data_command
    # app.cli.add_command(seed_data_command)
    return app