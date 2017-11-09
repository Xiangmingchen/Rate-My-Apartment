# This is how to query the database
from app import db
from app.models import Apartment, Address
from sqlalchemy import create_engine
from config import SQLALCHEMY_DATABASE_URI
from sqlalchemy.orm import sessionmaker

engine = create_engine(SQLALCHEMY_DATABASE_URI)
# Base.metadata.bind = engine
#
# DBSession = sessionmaker()
# DBSession.bind = engine
session = db.session()
# To print zpid, address, rent per month
# the linked tables can be accessed now
'''
for apartment in session.query(Apartment).all():
    print('zpid:', apartment.zpid, \
          '\nAddress:', apartment.address[0].street, \
                        apartment.address[0].city, \
                        apartment.address[0].state, \
                        apartment.address[0].zipcode, \
          '\nRent per month:', apartment.rentPerMonth, '\n')


# Printing all the zpid of Apartments
for zpid in session.query(Apartment.zpid):
     print(zpid)
'''
