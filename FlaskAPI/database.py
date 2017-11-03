import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Address(Base):
    __tablename__ = 'address'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    street = Column(String(250))
    zipcode = Column(Integer, nullable=False)
    city = Column(String(50))
    state = Column(String(20))
    apartment_id = Column(Integer, ForeignKey('apartment.id'))

class Apartment(Base):
    __tablename__ = 'apartment'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    zpid = Column(Integer, nullable=False)
    address = relationship('Address', backref='apartment')
    rentPerMonth = Column(Float)


# Create an engine that stores data in the local directory's
# sqlalchemy_example.db file.
engine = create_engine('sqlite:///apartments.db')

# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
Base.metadata.create_all(engine)
