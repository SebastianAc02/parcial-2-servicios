from flask import Flask
from .config import Config, TestingConfig


def create_app(testing=False):
    app = Flask(__name__)
    app.config.from_object(TestingConfig() if testing else Config())

    from .routes.external import external_bp
    app.register_blueprint(external_bp, url_prefix='/external')

    return app
