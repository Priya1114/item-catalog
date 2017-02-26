from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()
class User(Base):
    # Table to add the Users data
    __tablename__ = 'user'

    name = Column(String(250), nullable=False)
    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))
    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'name'         : self.name,
           'email'         : self.email,
           'id'         : self.id,
           'picture'         : self.picture,
       }


class Catalog(Base):
    # Table to add catalog
    __tablename__ = 'catalog'

    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'name'         : self.name,
           'id'           : self.id,
           'user_id'      : self.user_id,

       }


class CatalogItem(Base):
    # Table to add Caralog Items
    __tablename__ = 'menu_item'

    title = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    description = Column(String(250))
    catalog_id = Column(Integer, ForeignKey('catalog.id'))
    user_id = Column(Integer, ForeignKey('user.id'))
    category = Column(String(250))
    catalog = relationship(Catalog)
    user = relationship(User)


    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'title'         : self.title,
           'description'   : self.description,
           'id'            : self.id,
           'category'      : self.category,
           'user name'       : self.user_id

       }


engine = create_engine('sqlite:///catalogitemswithusers.db')

Base.metadata.create_all(engine)

