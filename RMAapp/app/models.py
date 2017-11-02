from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship
from app.database import Base


class Apartment(Base):
    __tablename__ = 'apartment'
    # Here we define columns for the table Apartment
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    zpid = Column(Integer, nullable=False)
    address = relationship('Address', backref='apartment')
    rentPerMonth = Column(Float)

class Address(Base):
    __tablename__ = 'address'
    # Here we define columns for the table address.
    id = Column(Integer, primary_key=True)
    street = Column(String(250))
    zipcode = Column(Integer, nullable=False)
    city = Column(String(50))
    state = Column(String(20))
    apartment_id = Column(Integer, ForeignKey('apartment.id'))
