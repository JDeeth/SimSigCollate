from flask import url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.schema import UniqueConstraint

db = SQLAlchemy()


class SimSigServer(db.Model):
    """
    Represents a connection to a SimSig game.
    Autoincrement turned on against Sqlite's advice to prevent repeated
    deletion of a server from deleting subsequent servers
    """

    __tablename__ = "simsig_servers"
    __table_args__ = (
        UniqueConstraint("uri_host", "uri_port", name="uri_uc"),
        {"sqlite_autoincrement": True},
    )

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    sim = db.Column(db.String)
    uri_host = db.Column(db.String, nullable=False)
    uri_port = db.Column(db.Integer, nullable=False, default=51515)

    @property
    def url(self):
        """For HTTP 201, to return the location of a created resource"""
        return url_for("get_server", id=self.id)
