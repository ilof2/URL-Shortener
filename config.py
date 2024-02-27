""" All configs stored here """
from os import environ, path
from dataclasses import dataclass

BASE_DIR = path.abspath(path.dirname(__file__))


@dataclass
class Config:
    """ Base configuration class. """
    TESTING: bool = False
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    SERVER_NAME: str = "localhost:8000"


@dataclass
class ProductionConfig(Config):
    """Production configuration class"""
    NAME: str = "prod"
    SQLALCHEMY_DATABASE_URI: str = environ.get("SQLALCHEMY_DATABASE_URI", "")
    CELERY_BROKER_URL: str = environ.get("CELERY_BROKER_URL", "")
    CELERY_RESULT_BACKEND: str = environ.get("CELERY_RESULT_BACKEND", "")
    CELERY_IGNORE_RESULT: bool = True
    BROKER_CONNECTION_RETRY_ON_STARTUP: bool = True


@dataclass
class DevelopmentConfig(Config):
    """ Development configuration class. Use only locally """
    NAME: str = "dev"
    SQLALCHEMY_DATABASE_URI: str = environ.get(
        "SQLALCHEMY_DATABASE_URI",
        default=f"sqlite:///{path.join(BASE_DIR, 'url_short.db')}"
    )
    CELERY_BROKER_URL: str = environ.get("CELERY_BROKER_URL", "redis://redis")
    CELERY_RESULT_BACKEND: str = environ.get("CELERY_RESULT_BACKEND", "redis://redis")
    CELERY_IGNORE_RESULT: bool = True
    BROKER_CONNECTION_RETRY_ON_STARTUP: bool = True
    TESTING: bool = True


@dataclass
class TestingConfig(Config):
    """ Testing configuration class. Use only for the testing """
    NAME: str = "test"
    SQLALCHEMY_DATABASE_URI: str = environ.get("SQLALCHEMY_DATABASE_URI", 'sqlite:///:memory:')
    CELERY_BROKER_URL: str = environ.get("CELERY_BROKER_URL", "redis://redis")
    CELERY_RESULT_BACKEND: str = environ.get("CELERY_RESULT_BACKEND", "redis://redis")
    CELERY_IGNORE_RESULT: bool = True
    BROKER_CONNECTION_RETRY_ON_STARTUP: bool = True
    TESTING: bool = True


CONFIGS_LIST: tuple = (
    ProductionConfig,
    DevelopmentConfig,
    TestingConfig,
)

config_by_name = {config.NAME: config for config in CONFIGS_LIST}
