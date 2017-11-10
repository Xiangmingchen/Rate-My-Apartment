from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reviewdata.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from app import view
from app.database import db_session

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


