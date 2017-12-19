from flask_script import Manager
from RMAapp.app import app, db
from RMAapp.config import DevelopmentConfig, ProductionConfig

app.config.from_object(DevelopmentConfig)
manager = Manager(app)

if __name__ == '__main__':
    manager.run()
