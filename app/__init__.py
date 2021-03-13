from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from marshmallow.exceptions import ValidationError

from config import Config
from app.models import db, SimSigServer
from app.schemas import ma, servers_schema, server_schema

# pylint: disable=redefined-builtin


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
    def get_server(id):
        server = SimSigServer.query.get_or_404(id)
        return server_schema.jsonify(server)

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
            response = jsonify({"message": "uri already added"})
            response.status_code = 400
            return response

        response = jsonify({"message": "created"})
        response.headers["location"] = server.url
        response.status_code = 201
        return response

    @app.route("/servers/<int:id>", methods=["DELETE"])
    def delete_server(id):
        server = SimSigServer.query.get_or_404(id)
        db.session.delete(server)
        db.session.commit()
        return jsonify({"message": "deleted"})

    @app.errorhandler(404)
    def page_not_found(_):
        resp = jsonify({"error": "not found"})
        resp.status_code = 404
        return resp

    return app


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all()
        app.run()
