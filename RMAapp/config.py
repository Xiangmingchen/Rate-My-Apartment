import os
basedir = os.path.abspath(os.path.dirname(__file__))

class BaseConfig():
    WTF_CSRF_ENABLED = True
    SECRET_KEY = 'ratemyapartment'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app', 'apartments.db')
    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'database_migration')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig(BaseConfig):
    DEBUG = False
    SQLALCHEMY_MIGRATE_REPO = './database_migration' # this may not work 
    SQLALCHEMY_TRACK_MODIFICATIONS = False
