from flask import Flask
from celery import Celery, Task
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


def celery_init_app(app: Flask) -> Celery:
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_config_object = dict(
        broker_url=app.config["CELERY_BROKER_URL"],
        result_backend=app.config["CELERY_RESULT_BACKEND"],
        task_ignore_result=app.config["CELERY_IGNORE_RESULT"],
        broker_connection_retry_on_startup=app.config["BROKER_CONNECTION_RETRY_ON_STARTUP"]
    )
    celery_app.config_from_object(celery_config_object)
    celery_app.set_default()
    app.extensions["celery"] = celery_app
    return celery_app


db = SQLAlchemy(model_class=Base)
migrate = Migrate(render_as_batch=True)
