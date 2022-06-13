import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or "NEISNF$*#(424FS75J"
    # In the previous line we used or to have a default value beside the os.environ
    # We will never share the secret key so this must be taken from .env file
    # during the production phase!
    # but for ease of use in development phase we have set a default key...

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQL_DATABASE_URL = os.environ.get('DEV_DATABASE_URL') or \
                       os.path.join(basedir, 'app', 'database', 'database.db')


class TestingConfig(Config):
    TESTING = True
    SQL_DATABASE_URL = os.environ.get('TEST_DATABASE_URL') or \
                       'sqlite://'


class ProductionConfig(Config):
    SQL_DATABASE_URL = os.environ.get('DATABASE_URL')
    # This should be driven from the database path on the pythonanywhere sever...


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
