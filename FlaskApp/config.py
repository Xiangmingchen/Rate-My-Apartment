import os
basedir = os.path.abspath(os.path.dirname(__file__))

WTF_CSRF_ENABLED = True
SECRET_KEY = 'Meow---meow'

OPENID_PROVIDERS = [
    {'name' : 'Google', 'url': 'https://myaccount.google.com'},
    {'name' : 'Yahoo', 'url' : 'http://openid.yahoo.com'}
]

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
