import os
import logging
from logging.handlers import RotatingFileHandler
from flask.logging import default_handler


def change_logger(app):
    formatter = logging.Formatter("%(asctime)s.%(msecs)03d| %(levelname)-8s| %(message)s")
    logLevel = logging.DEBUG if app.config["TESTING"] else logging.INFO

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    stream_handler.setLevel(logLevel)

    logs_folder = "./logs"
    if not os.path.exists(logs_folder):
        os.mkdir(logs_folder)

    file_handler = RotatingFileHandler("./logs/url_shortener.log", backupCount=5, maxBytes=10000)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logLevel)

    app.logger.removeHandler(default_handler)
    for logger in (
        app.logger,
        logging.getLogger(),
        logging.getLogger("sqlalchemy"),
    ):
        logger.handlers.clear()
        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)
