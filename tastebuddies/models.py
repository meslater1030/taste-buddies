# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from sqlalchemy import (
    Table,
    Column,
    Integer,
    Text,
    ForeignKey,
    Boolean,
    PickleType
)


from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    relationship,
    validates,
)

from pyramid.security import Allow

from zope.sqlalchemy import ZopeTransactionExtension


DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()

group_user = Table('group_user', Base.metadata,
                   Column('group_id', Integer, ForeignKey('groups.id')),
                   Column('user_id', Integer, ForeignKey('users.id'))
                   )


class TableSetup(object):
    id = Column(Integer, primary_key=True, autoincrement=True)

    @classmethod
    def add(cls, session=None, **kwargs):
        if session is None:
            session = DBSession
        instance = cls(**kwargs)
        session.add(instance)
        return instance

    @classmethod
    def all(cls, session=None):
        if session is None:
            session = DBSession
        return session.query(cls).all()

    @classmethod
    def lookup_by_attribute(cls, session=None, **kwargs):
        if session is None:
            session = DBSession
        return session.query(cls).filter_by(**kwargs).all()

    @classmethod
    def edit(cls, session=None, **kwargs):
        if session is None:
            session = DBSession
        instance = cls(**kwargs)
        session.query(cls).filter(cls.id == kwargs['id']).update(kwargs)
        return instance

    @classmethod
    def delete(cls, session=None, **kwargs):
        if session is None:
            session = DBSession
        instance = cls(**kwargs)
        session.query(cls).filter(cls.id == kwargs['id']).delete()
        return instance


class User(Base, TableSetup):
    __tablename__ = 'users'
    username = Column(Text, nullable=False, unique=True)
    password = Column(Text, nullable=False)
    email = Column(Text, nullable=False, unique=True)
    firstname = Column(Text)
    lastname = Column(Text)
    confirmed = Column(Boolean, default=False)
    ver_code = Column(Integer)
    restaurants = Column(Text)
    food = Column(Text)
    criteria_id = Column(Integer, ForeignKey('criteria.id'))
    admin_groups = relationship("Group", backref='admin')

    @validates('email')
    def validate_email(self, key, email):
        try:
            assert '@' in email
            assert '.' in email
            return email
        except:
            raise TypeError('Please enter a vaild email address')

    # I think this can also be replaced by edit.  Maybe turn the string
    # into an integer in views?
    @classmethod
    def write_ver_code(cls, username, ver_code, session=None):
        if session is None:
            session = DBSession
        instance = cls.lookup_by_attribute(username=username)[0]
        instance.ver_code = int(ver_code)
        session.add(instance)
        return instance

    # ditto the above.
    @classmethod
    def confirm_user(cls, username, session=None):
        if session is None:
            session = DBSession
        instance = cls.lookup_by_attribute(username=username)[0]
        instance.confirmed = True
        session.add(instance)
        return instance

    @property
    def __acl__(self):
        acl = []
        acl.append((Allow, self.username, 'owner'))
        for group in self.groups:
            acl.append((Allow, 'group:{}'.format(group.id), 'connect'))
        return acl

    def __repr__(self):
        return "<User({} {}, username={})>".format(self.firstname,
                                                   self.lastname,
                                                   self.username)


class Criteria(Base, TableSetup):
    """Constant variables are used to generate options for the user
    to choose from on the front end.  Columns are PickleTypes and expect
    to receive and return lists.  Each user has one set of criteria and
    each group has one set of criteria and vice versa for a one to one
    relationship.
    """
    __tablename__ = 'criteria'
    TASTES = ['Sour', 'Sweet', 'Salty', 'Spicy', 'Bitter', 'Italian',
              'Chinese', 'American Classic', 'German', 'British',
              'French', 'Vietnamese', 'Japanese', 'Pub', 'Persian',
              'Mediterranian', 'Greek', 'Afghan', 'Somolian',
              'Thai', 'Barbecue', 'Soul', 'Ethiopian', 'Jamaican',
              'Mexican', 'Korean',
              ]
    DIETS = ['Vegetarian', 'Vegan', 'Gluten Free', 'Low Carb']
    LOCATIONS = ['Seattle', 'Kitsap', 'Eastside', 'Skagit', 'South King']
    AGES = ['18-24', '25-34', '35-44', '45-54', '55-64', '65-74', '75+']
    COSTS = ['$', '$$', '$$$', '$$$$']
    taste = Column(PickleType)
    age = Column(PickleType)
    location = Column(PickleType)
    cost = Column(PickleType)
    diet = Column(PickleType)
    group = relationship('Group', uselist=False, backref='criteria')
    user = relationship('User', uselist=False, backref='criteria')

    def __repr__(self):
        if self.user:
            return"<Criteria for %s>" % (self.user.username)
        else:
            return"<Criteria for %s>" % (self.group.name)


class Group(Base, TableSetup):
    """We expect forum to be input as a dictionary where keys
    represent titles and values are a list of posts.
    """
    __tablename__ = 'groups'
    name = Column(Text, unique=True, nullable=False)
    description = Column(Text, nullable=False)
    forum = Column(PickleType)
    admin_id = Column(Integer, ForeignKey('users.id'))
    criteria_id = Column(Integer, ForeignKey('criteria.id'))
    users = relationship("User", secondary=group_user, backref='groups')

    @property
    def __acl__(self):
        acl = []
        acl.append((Allow, self.admin, 'g_admin'))
        members = self.id.users
        for member in members:
            acl.append((Allow, 'member:{}'.format(member.username), 'member'))
        return acl

    def __repr__(self):
        return "<Group(%s)>" % (self.name)
