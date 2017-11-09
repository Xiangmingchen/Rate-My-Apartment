from sqlalchemy import Column, ForeignKey, Integer, String, Float, Text
from sqlalchemy.orm import relationship
from app import db


class Apartment(db.Model):
    __tablename__ = 'apartment'
    # Here we define columns for the table Apartment
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    zpid = Column(Integer, nullable=False)
    address = relationship('Address', backref='apartment')
    rentPerMonth = Column(Float)
    image = relationship('Image', backref='apartment')
    review = relationship('Review', backref='apartment')

    def __repr__(self):
        return '<Apartment %r>' % (self.id)

class Address(db.Model):
    __tablename__ = 'address'
    # Here we define columns for the table address.
    id = Column(Integer, primary_key=True)
    street = Column(String(250))
    zipcode = Column(Integer, nullable=False)
    city = Column(String(50))
    state = Column(String(20))
    apartment_id = Column(Integer, ForeignKey('apartment.id'))

    def __repr__(self):
        return '<Address %r>' % (self.street + ' ' + self.zipcode + ' ' + self.city + ' ' + self.state)

class Image(db.Model):
    __tablename__ = 'image'

    id = Column(Integer, primary_key=True)
    url = Column(Text, nullable=False)
    apartment_id = Column(Integer, ForeignKey('apartment.id'))

    def __repr__(self):
        return '<URL %r>' % (self.url)

class Review(db.Model):
    __tablename__ = 'review'

    id = Column(Integer, primary_key=True)
    user_name = Column(String(50), nullable=False)
    content = Column(Text, nullable=False)
    apartment_id = Column(Integer, ForeignKey('apartment.id'))

    def __repr__(self):
        return '<Review from user: %r>' % (self.user_name)
