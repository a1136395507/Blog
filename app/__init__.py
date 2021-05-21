# coding=utf-8

import os
from flask import Flask
from config import config
# from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from .center._01_blog import bp as bp_demo
from app.utils.json_formater import JSONFormatter

# db = SQLAlchemy()

# 初始化登录操作
login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "Auth.login"


def create_app(config_name):
    """
    初始化flask app ,config_name 为对于的环境名 DEV|PRD
    config_name : 环境名
    :return:
    """
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    app.config['JSON_AS_ASCII'] = False
    config[config_name].init_app(app)

    # if not db.app:
    #     app.logger.debug("Create db.app:{} pid:{}".format(app, os.getpid()))
    #     db.app = app
    # db.init_app(app)
    login_manager.init_app(app)

    regist_blueprint(app)

    return app


def regist_blueprint(app):
    """
    应用启动前注册蓝图
    :param app:
    :return:

    注册蓝图，可以通过 http:127.0.0.1:5000/api/vi/domo 访问
    """

    app.register_blueprint(bp_demo,url_prefix="/" + bp_demo.name)