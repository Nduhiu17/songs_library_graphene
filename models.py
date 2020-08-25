import graphene
from sqlalchemy import *
from sqlalchemy.orm import (scoped_session, sessionmaker, relationship, backref)

from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///database.sqlite3', convert_unicode=True)

db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()


class Artist(Base):
    __tablename__ = 'artists'

    uuid = Column(Integer, primary_key=True)
    name = Column(String(256), index=True, unique=True)

    def __repr__(self):
        return '<Artist %r>' % self.name


class Song(Base):
    __tablename__ = 'songs'
    uuid = Column(Integer, primary_key=True)
    title = Column(String(256), index=True)
    description = Column(Text)
    author_id = Column(Integer, ForeignKey('artists.uuid'))
    author = relationship(
        Artist,
        backref=backref('songs',
                        cascade='delete,all'
                        ))

    def __repr__(self):
        return '<Song %r>' % self.title

