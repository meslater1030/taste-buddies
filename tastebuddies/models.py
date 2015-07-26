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
                   Column('groups', Integer, ForeignKey('groups.id')),
                   Column('users', Integer, ForeignKey('users.id'))
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
    groups = relationship('Group', secondary=group_user, backref='users')
    restaurants = Column(Text)
    food = Column(Text)
    criteria_id = Column(Integer, ForeignKey('criteria.id'))

    @validates('email')
    def validate_email(self, key, email):
        try:
            assert '@' in email
            assert '.' in email
            return email
        except:
            raise TypeError('Please enter a vaild email address')

    # I think this can be replaced by edit
    @classmethod
    def addgroup(cls, session=None, usergroup=None, username=None):
        if session is None:
            session = DBSession
        instance = cls.lookup_by_attribute(username=username)[0]
        instance.groups.append(usergroup)
        session.add(instance)
        return instance

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
    taste = Column(PickleType)  # many for groups and users
    age = Column(PickleType)  # many for groups, one for users
    location = Column(PickleType)  # one for both
    cost = Column(PickleType)  # many for both
    diet = Column(PickleType)  # many for both
    group = relationship('Group', uselist=False, backref='criteria')
    user = relationship('User', uselist=False, backref='criteria')

    def __repr__(self):
        if self.user:
            return"<Criteria(%s)>" % (self.user.username)
        else:
            return"<Criteria(%s)>" % (self.group.name)


class Group(Base, TableSetup):
    __tablename__ = 'groups'
    name = Column(Text, unique=True, nullable=False)
    description = Column(Text, nullable=False)
    discussions = relationship('Discussion',
                               primaryjoin="(Group.id==Discussion.group_id)")
    admin = relationship("Admin", uselist=False)
    criteria_id = Column(Integer, ForeignKey('criteria.id'))

    @classmethod
    def edit(cls, session=None, **kwargs):
        if session is None:
            session = DBSession
        instance = cls.lookup_by_attribute(id=kwargs["id"])[0]
        instance.name = kwargs.get("name")
        instance.description = kwargs.get("description")
        if kwargs.get("discussions"):
            instance.discussions = kwargs.get("discussions")
        session.add(instance)
        return instance

    @property
    def __acl__(self):
        acl = []
        acl.append((Allow, self.admin, 'g_admin'))
        members = self.id.users
        for member in members:
            acl.append((Allow, 'member:{}'.format(member.username), 'member'))
        return acl

    def __repr__(self):
        return "<Group(%s, location=%s)>" % (self.name, self.location)


class Discussion(Base, TableSetup):
    __tablename__ = 'discussion'
    title = Column(Text)
    group_id = Column(Integer, ForeignKey('groups.id'))
    posts = relationship('Post',
                         primaryjoin="(Discussion.id==Post.discussion_id)")

    def __repr__(self):
        return "<Discussion(%s)>" % (self.title)


class Post(Base, TableSetup):
    __tablename__ = 'post'
    text = Column(Text)
    discussion_id = Column(Integer, ForeignKey('discussion.id'))

    def __repr__(self):
        return "<Post(%s)>" % (self.text)


class Admin(Base, TableSetup):
    __tablename__ = 'admin'
    users = Column(Integer, ForeignKey('users.id'))
    group_id = Column(Integer, ForeignKey('groups.id'))

    def __repr__(self):
        return "<Admin(%s)>" % (self.users)
