import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config():
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
    LOG_FOLDER = os.path.join(basedir, 'logs')
    HOST = "0.0.0.0"
    PORT = 5000

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    ENV = "dev"


class ProductionConfig(Config):
    DEBUG = False
    ENV = "prd"


config = {
    'dev': DevelopmentConfig,
    'prd': ProductionConfig,

}
