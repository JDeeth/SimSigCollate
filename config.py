import os


class Config:
    # pylint: disable=missing-class-docstring
    SECRET_KEY = os.environ.get("SECRET_KEY") or "collate_api_dev_key"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
