from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from RMAapp.config import DevelopmentConfig, ProductionConfig


app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
db = SQLAlchemy(app)

from RMAapp.app import view
