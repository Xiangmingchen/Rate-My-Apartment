from sqlalchemy import Column, ForeignKey, Integer, String, Float, Text, Boolean, DateTime
from sqlalchemy.orm import relationship
from app import db


class Apartment(db.Model):
    __tablename__ = 'apartment'
    # Here we define columns for the table Apartment
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    zpid = Column(Integer, nullable=False, unique=True)
    address = relationship('Address', backref='apartment', cascade='save-update, merge, delete')
    rentPerMonth = Column(Float)
    image = relationship('Image', backref='apartment', cascade='save-update, merge, delete')
    image_count = Column(Integer, default=0)
    review = relationship('Review', backref='apartment', cascade='save-update, merge, delete')
    comps = Column(Boolean, default=False)
    details = relationship('Details', backref='apartment', cascade='save-update, merge, delete')
    rooms = relationship('Rooms', backref='apartment', cascade='save-update, merge, delete')
    amentities = relationship('Amentities', backref='apartment', cascade='save-update, merge, delete')
    descripion = Column(String(2500))
    review_number = Column(Integer, default=0)
    average_rating = Column(Float, default=0)
    city_id = Column(Integer, ForeignKey('city.id'))

    def __repr__(self):
        return '<Apartment %r>' % str(self.id)

class City(db.Model):
    __tablename__ = 'city'
    # each city is related to the apartments in it
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    apartments = relationship('Apartment', backref='city', cascade='save-update, merge, delete')

    def __repr__(self):
        return '<City %r>' % str(self.name)

class Details(db.Model):
    __tablename__ = 'details'
    id = Column(Integer, primary_key=True)
    apartment_id = Column(Integer, ForeignKey('apartment.id'))
    bedrooms = Column(Integer)
    bathrooms = Column(Float)
    area = Column(Integer)
    lot_area = Column(Integer)
    year_built = Column(Integer)
    year_update = Column(Integer)
    num_floor = Column(Integer)
    basement = Column(String(20))
    view = Column(String(100))
    parking_type = Column(String(20))
    heating_source = Column(String(20))
    heating_system = Column(String(20))
    cooling_system = Column(String(20))

class Rooms(db.Model):
    __tablename__ = 'rooms'
    id = Column(Integer, primary_key=True)
    apartment_id = Column(Integer, ForeignKey('apartment.id'))
    name = Column(String(30))

    def __repr__(self):
        return '<Room %r>' % str(self.name)

class Amentities(db.Model):
    __tablename__ = 'amentities'
    id = Column(Integer, primary_key=True)
    apartment_id = Column(Integer, ForeignKey('apartment.id'))
    name = Column(String(30))

    def __repr__(self):
        return '<Amentities %r>' % str(self.name)

class Address(db.Model):
    __tablename__ = 'address'
    # Here we define columns for the table address.
    id = Column(Integer, primary_key=True)
    street = Column(String(250))
    zipcode = Column(Integer, nullable=False)
    city = Column(String(50))
    state = Column(String(20))
    latitude = Column(Float)
    longitude = Column(Float)
    apartment_id = Column(Integer, ForeignKey('apartment.id'))

    def __repr__(self):
        return '<Address %r>' % (self.street + ' ' + str(self.zipcode) + ' ' + self.city + ' ' + self.state)

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
    rating = Column(Float, default=0)
    time_stamp = Column(DateTime)
    apartment_id = Column(Integer, ForeignKey('apartment.id'))

    def __repr__(self):
        return '<Review from user: %r>' % (self.user_name)
