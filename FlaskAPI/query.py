# This is how to query the database
from database import Apartment, Base, Address
from sqlalchemy import create_engine
engine = create_engine('sqlite:///apartments.db')
Base.metadata.bind = engine
from sqlalchemy.orm import sessionmaker
DBSession = sessionmaker()
DBSession.bind = engine
session = DBSession()
# To print zpid, address, rent per month
# the linked tables can be accessed now
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
