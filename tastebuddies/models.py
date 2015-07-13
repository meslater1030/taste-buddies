from sqlalchemy import (
    Table,
    Column,
    Index,
    Integer,
    Text,
    ForeignKey
    )

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    relationship,
    backref
    )

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


usertaste_table = Table('user_profile', Base.metadata,
                        Column('user', Integer, ForeignKey('user.id')),
                        Column('profile', Integer, ForeignKey('profile.id'))
                        )


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(Text)
    firstname = Column(Text)
    lastname = Column(Text)
    password = Column(Text)
    food_profile = relationship("Profile", secondary=usertaste_table,
                                backref="profiles")
    restaurants = Column(Text)
    photo = Column(Text)


class Profile(Base):
    __tablename__ = 'profile'
    id = Column(Integer, primary_key=True)
    Spicy = Column(Text)
    Sweet = Column(Text)
    Savory = Column(Text)
    Bitter = Column(Text)
    Sour = Column(Text)
