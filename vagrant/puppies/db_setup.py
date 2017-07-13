import sys
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, LargeBinary
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class Shelter(Base):
    __tablename__ = 'shelter'

    name = Column(String(80), nullable = False)
    address = Column(String(250), nullable = False)
    city = Column(String(80))
    state = Column(String(20))
    zipCode = Column(String(10))
    website = Column(String(250))
    id = Column(Integer, primary_key = True)

class MenuItem(Base):
    __tablename__ = 'menu_item'

    name = Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)
    dob = Column(DateTime)
    sex = Column(String(6), nullable = False)
    weight = Column(Integer, nullable = False)
    picture = Column(LargeBinary())
    shelter_id = Column(Integer, ForeignKey('shelter.id'))
    shelter = relationship(Shelter)


####### insert at end of file ######

engine = create_engine(
'sqlite:///puppies.db')

Base.metadata.create_all(engine)
