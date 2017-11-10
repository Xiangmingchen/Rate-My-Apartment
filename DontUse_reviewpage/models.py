from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship
from app.database import Base


class Review(Base):
    __tablename__ = 'review'
    review_id = Column(String(250), index=True, primary_key=True)
    nickname = Column(String(250))
    rating = Column(Integer)
    comments = Column(String(500))


apartments = relationship('Apartments', backref='Review')