# coding=utf-8

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from app.utils.json_formater import JSONFormatter
from config.config import config_map
db = SQLAlchemy()

# 初始化登录操作
login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "Auth.login"


def configure_logging(app):
    """Configure file(info) and email(error) logging."""
    import os
    import logging
    from logging.handlers import RotatingFileHandler
    from flask.logging import default_handler

    app.logger.setLevel(logging.INFO)
    if not os.path.isdir(app.config['LOG_FOLDER']):
        os.makedirs(app.config['LOG_FOLDER'])

    format_str = "%(asctime)s %(levelname)s %(process)d %(thread)d %(filename)s-%(funcName)s:%(lineno)d %(message)s"
    format = logging.Formatter(format_str)
    info_log = os.path.join(app.config['LOG_FOLDER'], 'info.log')
    info_file_handler = RotatingFileHandler(info_log, maxBytes=100000, backupCount=10)
    info_file_handler.setLevel(logging.INFO)
    info_file_handler.setFormatter(format)
    app.logger.addHandler(info_file_handler)

    error_log = os.path.join(app.config['LOG_FOLDER'], 'error.log')
    error_file_handler = RotatingFileHandler(error_log, maxBytes=100000, backupCount=10)
    error_file_handler.setLevel(logging.ERROR)
    app.logger.addHandler(error_file_handler)
    app.logger.removeHandler(default_handler)


def create_app(config_name='dev'):
    """
    初始化flask app ,config_name 为对于的环境名 DEV|PRD
    config_name : 环境名
    :return:
    """
    app = Flask(__name__)
    app.config.from_object(config_map[config_name])
    app.config['JSON_AS_ASCII'] = False
    # config[config_name].init_app(app)

    if not db.app:
        app.logger.debug("Create db.app:{} pid:{}".format(app, os.getpid()))
        db.app = app
    db.init_app(app)
    login_manager.init_app(app)
    configure_logging(app)

    return app

