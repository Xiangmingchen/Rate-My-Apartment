import os
import sys

from sqlalchemy import create_engine
from sqlalchemy import Column, ForeignKey, Integer, String, Float, Boolean, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, scoped_session, sessionmaker, backref

engine = create_engine('sqlite:////reviewdata.db', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

# from __init__ import db

Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    from app import models
    Base.metadata.create_all(bind=engine)



from reviewdata.database import db_session

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

# This last line creates a .reviews attribute for Restaurant. The backref argument also creates a .restaurant attribute
# for class Review. This is syntactic sugar that allows me to set up the whole relationship in this line, without
# specifying the relationship in the class Review.







