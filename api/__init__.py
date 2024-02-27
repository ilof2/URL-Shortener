from os import environ

from flask import Flask, redirect
from flask_restx import Api, abort
from flask_restx.utils import HTTPStatus

from config import config_by_name
from api.routes import register_routes
from .extensions import db, migrate
from .logger import change_logger


def get_settings(env: str | None):
    """Return setting class by FLASK_SETTING env variable"""

    setting_name: str = env or environ.get("FLASK_SETTING", "dev")
    return config_by_name.get(setting_name)


def create_app(env: str | None = None):
    """ Application factory function """

    app = Flask(__name__)
    change_logger(app)

    api = Api(app, title="URLShortener", version="0.1.0")
    settings = get_settings(env)
    app.config.from_object(settings)

    register_routes(api)

    # Make models visible for Migrate tool
    import api.models as app_models

    # Extensions init
    db.init_app(app)
    migrate.init_app(app, db)

    @app.route("/<string:url_id>", methods=["GET"])
    def index(url_id: str):
        url = app_models.URL.query.filter_by(short_url=url_id).first()
        if not url:
            return abort(HTTPStatus.NOT_FOUND)

        return app.redirect(url.old_url)

    return app
