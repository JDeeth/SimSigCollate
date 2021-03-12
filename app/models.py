from flask import url_for
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class SimSigServer(db.Model):
    """
    Represents a connection to a SimSig game.
    """

    __tablename__ = "simsig_servers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    sim = db.Column(db.String)
    uri_host = db.Column(db.String, nullable=False)
    uri_port = db.Column(db.Integer, nullable=False)

    @property
    def url(self):
        """For HTTP 201, to return the location of a created resource"""
        return url_for("get_server", id=self.id)
