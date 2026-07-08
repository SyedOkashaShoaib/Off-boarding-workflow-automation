from flask import Flask
from config import Config
from app.extension import db, migrate
from routes.case_routes import case_bp
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.register_blueprint(case_bp)
    db.init_app(app)
    migrate.init_app(app, db)

    from app import models
    return app