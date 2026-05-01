from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config, TestingConfig

db = SQLAlchemy()


def create_app(testing=False):
    app = Flask(__name__)
    app.config.from_object(TestingConfig() if testing else Config())

    db.init_app(app)

    from .routes.notes import notes_bp
    app.register_blueprint(notes_bp, url_prefix='/notes')

    with app.app_context():
        db.create_all()

    return app
