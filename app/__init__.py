from flask import Flask
from config import Config
from app.extension import db, migrate

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    migrate.init_app(app)

    from app import models
    return app