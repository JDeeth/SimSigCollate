"""
Marshmallow schemas, copied unapologetically from David Baumgold
Note - Marshmallow has moved on since then, `ModelSchema` is deprecated.
"""
from flask_marshmallow import Marshmallow
from app.models import SimSigServer

ma = Marshmallow()


# pylint: disable=too-many-ancestors
class ServerSchema(ma.SQLAlchemyAutoSchema):
    """ Will need to hide IP addresses from general viewers """

    class Meta:  # pylint: disable=missing-class-docstring
        model = SimSigServer
        load_instance = True


server_schema = ServerSchema()
servers_schema = ServerSchema(many=True)
