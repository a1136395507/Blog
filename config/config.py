import os
from config import DB_USER_INFO_MYSQL,DB_BLOG_PRODUCT_MYSQL,DB_URL
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """
    基础配置
    """
    DEBUG = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'this is a complicated string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_POOL_SIZE = 200
    SQLALCHEMY_POOL_RECYCLE = 3600
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_recycle': 280,
        'pool_timeout': 300,
        'pool_size': 50,
        'max_overflow': 5,

    }
    SQL_USER_POOL = DB_USER_INFO_MYSQL.PYMYSQL_POOL
    SQL_PRODUCT_POOL = DB_BLOG_PRODUCT_MYSQL.PYMYSQL_POOL
    LOG_FOLDER = os.path.join(basedir, 'logs')
    HOST = "0.0.0.0"
    PORT = 5000
    SQLALCHEMY_DATABASE_URI = DB_URL

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    """测试环境"""
    DEBUG = True
    ENV = "dev"


class ProductionConfig(Config):
    """ 生产环境"""
    DEBUG = False
    ENV = "prd"


config_map = {
    'dev': DevelopmentConfig,
    'prd': ProductionConfig,

}
