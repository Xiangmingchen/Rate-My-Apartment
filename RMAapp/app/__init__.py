from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

from app import view
from app.database import db_session

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()
