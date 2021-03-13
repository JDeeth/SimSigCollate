import os


class Config:
    # pylint: disable=missing-class-docstring
    SECRET_KEY = os.environ.get("SECRET_KEY") or "collate_api_dev_key"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL"
    ) or "sqlite:///" + os.path.join(
        os.path.abspath(os.path.dirname(__file__)), "app_db"
    )
