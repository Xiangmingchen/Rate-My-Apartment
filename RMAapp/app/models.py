from sqlalchemy import Column, ForeignKey, Integer, String, Float, Text, Boolean, DateTime
from sqlalchemy.orm import relationship
from app import db

# A class that represents Apartment table in the database
class Apartment(db.Model):
    __tablename__ = 'apartment'
    id            = Column(Integer, primary_key=True)
    zpid          = Column(Integer, nullable=False, unique=True)
    address       = relationship('Address', backref='apartment', cascade='save-update, merge, delete')
    rentPerMonth  = Column(Float)
    image         = relationship('Image', backref='apartment', cascade='save-update, merge, delete')
    image_count   = Column(Integer, default=0)
    review        = relationship('Review', backref='apartment', cascade='save-update, merge, delete')
    comps         = Column(Boolean, default=False)
    details       = relationship('Details', backref='apartment', cascade='save-update, merge, delete')
    rooms         = relationship('Rooms', backref='apartment', cascade='save-update, merge, delete')
    amentities    = relationship('Amentities', backref='apartment', cascade='save-update, merge, delete')
    descripion    = Column(String(2500))
    review_number = Column(Integer, default=0)
    average_rating = Column(Float, default=0)
    city_id       = Column(Integer, ForeignKey('city.id'))

    def __repr__(self):
        return '<Apartment %r>' % str(self.id)

# A class that represents City table in the database
# Each city is related to all the apartments in this city
# to make searching quicker
class City(db.Model):
    __tablename__ = 'city'
    id         = Column(Integer, primary_key=True)
    name       = Column(String, nullable=False)
    apartments = relationship('Apartment', backref='city', cascade='save-update, merge, delete')

    def __repr__(self):
        return '<City %r>' % str(self.name)

# A class that represents Details table in the database
# Each detail is related to an apartment, and stores
# all the detailed facts about this apartment
class Details(db.Model):
    __tablename__ = 'details'
    id           = Column(Integer, primary_key=True)
    apartment_id = Column(Integer, ForeignKey('apartment.id'))
    bedrooms     = Column(Integer)
    bathrooms    = Column(Float)
    area         = Column(Integer)
    lot_area     = Column(Integer)
    year_built   = Column(Integer)
    year_update  = Column(Integer)
    num_floor    = Column(Integer)
    basement     = Column(String(20))
    view         = Column(String(100))
    parking_type = Column(String(20))
    heating_source = Column(String(20))
    heating_system = Column(String(20))
    cooling_system = Column(String(20))

# A class that represents Rooms table in the database
# Multiple rooms are related to one apartment
# each describing a type of room
class Rooms(db.Model):
    __tablename__ = 'rooms'
    id           = Column(Integer, primary_key=True)
    apartment_id = Column(Integer, ForeignKey('apartment.id'))
    name         = Column(String(30))

    def __repr__(self):
        return '<Room %r>' % str(self.name)

# A class that represents Amentities table in the database
# Multiple amentities are related to one apartment
class Amentities(db.Model):
    __tablename__ = 'amentities'
    id           = Column(Integer, primary_key=True)
    apartment_id = Column(Integer, ForeignKey('apartment.id'))
    name         = Column(String(30))

    def __repr__(self):
        return '<Amentities %r>' % str(self.name)

# A class that represents Address table in the database
# each address is related to one apartment
class Address(db.Model):
    __tablename__ = 'address'
    # Here we define columns for the table address.
    id          = Column(Integer, primary_key=True)
    street      = Column(String(250))
    zipcode     = Column(Integer, nullable=False)
    city        = Column(String(50))
    state       = Column(String(20))
    latitude    = Column(Float)
    longitude   = Column(Float)
    apartment_id = Column(Integer, ForeignKey('apartment.id'))

    def __repr__(self):
        return '<Address %r>' % (self.street + ' ' + str(self.zipcode) + ' ' + self.city + ' ' + self.state)

# Each apartment is related to multiple images, which store the url
class Image(db.Model):
    __tablename__ = 'image'
    id           = Column(Integer, primary_key=True)
    url          = Column(Text, nullable=False)
    apartment_id = Column(Integer, ForeignKey('apartment.id'))

    def __repr__(self):
        return '<URL %r>' % (self.url)

# Each apartment is related to multiple reviews
class Review(db.Model):
    __tablename__ = 'review'
    id            = Column(Integer, primary_key=True)
    user_name     = Column(String(50), nullable=False)
    content       = Column(Text, nullable=False)
    rating        = Column(Float, default=0)
    time_stamp    = Column(DateTime)
    apartment_id  = Column(Integer, ForeignKey('apartment.id'))

    def __repr__(self):
        return '<Review from user: %r>' % (self.user_name)
