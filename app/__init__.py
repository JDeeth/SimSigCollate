from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

from config import Config
from app.models import db
from app.schemas import ma, server_schema


def create_app(config_class=Config):
    """Set up Flask app in a very standard way"""
    # pylint: disable=unused-variable,redefined-outer-name
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    ma.init_app(app)

    @app.route("/")
    def index():
        return jsonify()

    @app.route("/servers")
    def servers():
        return jsonify()

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
