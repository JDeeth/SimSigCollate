from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from marshmallow.exceptions import ValidationError

from config import Config
from app.models import db, SimSigServer
from app.schemas import ma, servers_schema, server_schema


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

    @app.route("/servers/")
    def list_servers():
        all_servers = SimSigServer.query.all()
        return servers_schema.jsonify(all_servers)

    @app.route("/servers/<int:id>")
    def get_server():
        pass

    @app.route("/servers/", methods=["POST"])
    def create_server():
        try:
            server = server_schema.load(request.form)
        except ValidationError as errors:
            response = jsonify(errors.messages)
            response.status_code = 400
            return response

        try:
            db.session.add(server)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            response = jsonify({"message": "uri not unique"})
            response.status_code = 400
            return response

        response = jsonify({"message": "created"})
        response.headers["location"] = server.url
        response.status_code = 201
        return response

    return app


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all()
        app.run()
