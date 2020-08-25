import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from models import Artist as ArtistModel, Song as SongModel

import graphene
from sqlalchemy import *
from sqlalchemy.orm import (scoped_session, sessionmaker)

from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///database.sqlite3', convert_unicode=True)

db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()


class Artist(SQLAlchemyObjectType):
    class Meta:
        model = ArtistModel
        interfaces = (relay.Node,)


class Song(SQLAlchemyObjectType):
    class Meta:
        model = SongModel
        interfaces = (relay.Node,)


class Query(graphene.ObjectType):
    node = relay.Node.Field()
    allSongs = SQLAlchemyConnectionField(Song.connection)
    all_artists = SQLAlchemyConnectionField(Artist.connection, sort=None)


class CreateArtist(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)

    artist = graphene.Field(lambda: Artist)

    def mutate(self,info, name):
        artist = ArtistModel(name=name)

        db_session.add(artist)
        db_session.commit()
        return CreateArtist(artist=artist)


class Mutation(graphene.ObjectType):
    create_artist = CreateArtist.Field()


schema = graphene.Schema(query=Query,mutation=Mutation)
