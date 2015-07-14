from sqlalchemy import (
    Table,
    Column,
    Integer,
    Text,
    ForeignKey,
    )

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    relationship,
    validates,
    )

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


usertaste_table = Table('user_profile', Base.metadata,
                        Column('users', Integer, ForeignKey('users.id')),
                        Column('profile', Integer, ForeignKey('profile.id'))
                        )


userdiet_table = Table('user_diet', Base.metadata,
                       Column('users', Integer, ForeignKey('users.id')),
                       Column('profile', Integer, ForeignKey('diet.id'))
                       )


usercost_table = Table('user_cost', Base.metadata,
                       Column('users', Integer, ForeignKey('users.id')),
                       Column('profile', Integer, ForeignKey('cost.id'))
                       )


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(Text, nullable=False, unique=True)
    firstname = Column(Text, nullable=False)
    lastname = Column(Text, nullable=False)
    password = Column(Text, nullable=False)
    email = Column(Text, nullable=False, unique=True)
    # age = Column(Integer, ForeignKey('agegroup.id'))
    # user_location = Column(Integer, ForeignKey('location.id'))
    # food_profile = relationship('profile', secondary=usertaste_table)
    # diet_restrict = relationship('diet', secondary=userdiet_table)
    # cost_restrict = relationship('cost', secondary=usercost_table)
    restaurants = Column(Text)
    photo = Column(Text)

    @validates('email')
    def validate_email(self, key, email):
        try:
            assert '@' in email
            assert '.' in email
            return email
        except:
            raise TypeError('Please enter a vaild email address')

    @classmethod
    def edit(cls, session=None, username=None, **kwargs):
        if session is None:
            session = DBSession
        instance = cls(**kwargs)
        session.query(cls).filter(cls.username == username).update(**kwargs)
        return instance

    @classmethod
    def write(cls, session=None, **kwargs):
        if session is None:
            session = DBSession
        instance = cls(**kwargs)
        session.add(instance)
        return instance

    @classmethod
    def lookup_user(cls, session=None, username=username):
        if session is None:
            session = DBSession
        return session.query(cls).get(username)

    def __repr__(self):
        return "<User({} {}, username={})>".format(self.firstname,
                                                   self.lastname,
                                                   self.username)


class Profile(Base):
    __tablename__ = 'profile'
    id = Column(Integer, primary_key=True, autoincrement=True)
    taste = Column(Text)


class AgeGroup(Base):
    __tablename__ = 'agegroup'
    id = Column(Integer, primary_key=True, autoincrement=True)
    age_group = Column(Text)


class Location(Base):
    __tablename__ = 'location'
    id = Column(Integer, primary_key=True, autoincrement=True)
    city = Column(Text)


class Cost(Base):
    __tablename__ = 'cost'
    id = Column(Integer, primary_key=True, autoincrement=True)
    cost = Column(Text)


class Diet(Base):
    __tablename__ = 'diet'
    id = Column(Integer, primary_key=True, autoincrement=True)
    diet = Column(Text)
