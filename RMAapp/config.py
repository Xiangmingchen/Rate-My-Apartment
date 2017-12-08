import os
basedir = os.path.abspath(os.path.dirname(__file__))


WTF_CSRF_ENABLED = True
SECRET_KEY = 'ratemyapartment'

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app', 'apartments.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'database_migration')

SQLALCHEMY_TRACK_MODIFICATIONS = False
