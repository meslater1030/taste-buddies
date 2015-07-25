# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from sqlalchemy import (
    Table,
    Column,
    Integer,
    Text,
    ForeignKey,
    Boolean,
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


user_taste = Table('user_taste', Base.metadata,
                   Column('users', Integer, ForeignKey('users.id')),
                   Column('taste', Integer, ForeignKey('taste.id'))
                   )


user_diet = Table('user_diet', Base.metadata,
                  Column('users', Integer, ForeignKey('users.id')),
                  Column('diet', Integer, ForeignKey('diet.id'))
                  )

group_user = Table('group_user', Base.metadata, Column('group', Integer,
                   ForeignKey('groups.id')), Column('users', Integer,
                   ForeignKey('users.id'))
                   )

group_taste = Table('group_taste', Base.metadata,
                    Column('group_id', Integer, ForeignKey('groups.id')),
                    Column('taste', Integer, ForeignKey('taste.id'))
                    )


group_diet = Table('group_diet', Base.metadata,
                   Column('group_id', Integer, ForeignKey('groups.id')),
                   Column('diet_id', Integer, ForeignKey('diet.id'))
                   )


class _Table(object):
    id = Column(Integer, primary_key=True, autoincrement=True)

    @classmethod
    def write(cls, session=None, **kwargs):
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
    def one(cls, eid=None, session=None):
        if session is None:
            session = DBSession
        return session.query(cls).filter(cls.id == eid).one()

    @classmethod
    def lookup_by_attribute(cls, session=None, **kwargs):
        if session is None:
            session = DBSession
        return session.query(cls).filter_by(**kwargs).one()


class User(Base, _Table):
    __tablename__ = 'users'
    username = Column(Text, nullable=False, unique=True)
    password = Column(Text, nullable=False)
    email = Column(Text, nullable=False, unique=True)
    firstname = Column(Text)
    lastname = Column(Text)
    confirmed = Column(Boolean, default=False)
    ver_code = Column(Integer)
    age = Column(Integer, ForeignKey('agegroup.id'))
    location = Column(Integer, ForeignKey('location.id'))
    cost = Column(Integer, ForeignKey('cost.id'))
    taste = relationship('Taste', secondary=user_taste, backref='users')
    diet = relationship('Diet', secondary=user_diet, backref='users')
    groups = relationship('Group', secondary=group_user, backref='users')
    restaurants = Column(Text)
    food = Column(Text)

    @validates('email')
    def validate_email(self, key, email):
        try:
            assert '@' in email
            assert '.' in email
            return email
        except:
            raise TypeError('Please enter a vaild email address')

    @classmethod
    def addgroup(cls, session=None, usergroup=None, username=None):
        if session is None:
            session = DBSession
        instance = cls.lookup_by_attribute(username=username)
        instance.groups.append(usergroup)
        session.add(instance)
        return instance

    @classmethod
    def write_ver_code(cls, username, ver_code, session=None):
        if session is None:
            session = DBSession
        instance = cls.lookup_by_attribute(username=username)
        instance.ver_code = int(ver_code)
        session.add(instance)
        return instance

    @classmethod
    def confirm_user(cls, username, session=None):
        if session is None:
            session = DBSession
        instance = cls.lookup_by_attribute(username=username)
        instance.confirmed = True
        session.add(instance)
        return instance

    @classmethod
    def change(cls, session=None, **kwargs):
        if session is None:
            session = DBSession
        instance = cls.lookup_by_attribute(username=kwargs["username"])
        instance.firstname = kwargs.get("firstname")
        instance.lastname = kwargs.get("lastname")
        instance.restaurants = kwargs.get("restaurant")
        instance.food = kwargs.get("food")
        tasteid = map(int, kwargs.get("taste"))
        dietid = map(int, kwargs.get("diet"))
        instance.taste = []
        instance.diet = []
        for eid in tasteid:
            instance.taste.append(session.query(Taste).filter
                                  (Taste.id == eid).all()[0])
        for eid in dietid:
            instance.diet.append(session.query(Diet).filter
                                 (Diet.id == eid).all()[0])

        instance.cost = int(kwargs.get("price"))
        instance.location = int(kwargs.get("location"))
        instance.age = int(kwargs.get("age"))

        session.add(instance)
        return instance

    @property
    def __acl__(self):
        acl = []

        acl.append((Allow, self.username, 'owner'))

        for group in self.groups:
            acl.append((Allow, 'group:{}'.format(group.id), 'connect'))

        # acl.append((Deny, Everyone, ALL_PERMISSIONS))

        return acl

    def __repr__(self):
        return "<User({} {}, username={})>".format(self.firstname,
                                                   self.lastname,
                                                   self.username)


class Taste(Base, _Table):
    __tablename__ = 'taste'
    taste = Column(Text, unique=True)

    def __repr__(self):
        return "<Taste(%s)>" % (self.taste)


class AgeGroup(Base, _Table):
    __tablename__ = 'agegroup'
    age_group = Column(Text)

    def __repr__(self):
        return "<Age(%s)>" % (self.age_group)


class Location(Base, _Table):
    __tablename__ = 'location'
    city = Column(Text)

    def __repr__(self):
        return "<Location(%s)>" % (self.city)


class Cost(Base, _Table):
    __tablename__ = 'cost'
    cost = Column(Text)

    def __repr__(self):
        return "<Cost(%s)>" % (self.cost)


class Diet(Base, _Table):
    __tablename__ = 'diet'
    diet = Column(Text)

    def __repr__(self):
        return "<Dietary Preference(%s)>" % (self.diet)


class Group(Base):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, unique=True, nullable=False)
    description = Column(Text, nullable=False)
    location = Column(Integer, ForeignKey('location.id'))
    discussions = relationship('Discussion',
                               primaryjoin="(Group.id==Discussion.group_id)")

    # group_admin = relationship("Admin", uselist=False, backref='group')
    group_admin = relationship("Admin", uselist=False)

    taste = relationship('Taste', secondary=group_taste,
                         backref='group')
    diet = relationship('Diet', secondary=group_diet, backref='group')
    cost = Column(Integer, ForeignKey('cost.id'))
    age = Column(Integer, ForeignKey('agegroup.id'))

    @classmethod
    def change(cls, session=None, **kwargs):
        if session is None:
            session = DBSession
        instance = cls.lookup_by_attribute(id=kwargs["id"])
        instance.name = kwargs.get("name")
        instance.description = kwargs.get("description")
        instance.location = int(kwargs.get("location"))
        if kwargs.get("discussions"):
            instance.discussions = kwargs.get("discussions")
        instance.age = int(kwargs.get("age"))
        instance.cost = int(kwargs.get("cost"))
        tasteid = map(int, kwargs.get("taste"))
        dietid = map(int, kwargs.get("diet"))
        instance.taste = []
        instance.diet = []
        for eid in tasteid:
            instance.taste.append(session.query(Taste).filter
                                  (Taste.id == eid).all()[0])
        for eid in dietid:
            instance.diet.append(session.query(Diet).filter
                                 (Diet.id == eid).all()[0])
        session.add(instance)
        return instance

    @classmethod
    def write(cls, session=None, **kwargs):
        if session is None:
            session = DBSession
        tasteid = map(int, kwargs.get("taste"))
        dietid = map(int, kwargs.get("taste"))
        grouptaste = []
        diettaste = []
        for eid in tasteid:
            grouptaste.append(session.query(Taste).filter
                              (Taste.id == eid).all()[0])
        for eid in dietid:
            diettaste.append(session.query(Diet).filter
                             (Diet.id == eid).all()[0])
        kwargs["taste"] = grouptaste
        kwargs["diet"] = diettaste
        username = kwargs.get("Admin")
        del kwargs['Admin']
        instance = cls(**kwargs)
        User.addgroup(usergroup=instance, username=username)
        session.add(instance)
        return instance

    @classmethod
    def all(cls, session=None):
        if session is None:
            session = DBSession
        return session.query(cls).all()

    @classmethod
    def get_members_of_gid(cls, gid, session=None):
        if session is None:
            session = DBSession

        return session.query(User).filter(User.groups == gid).all()

    @property
    def __acl__(self):
        acl = []

        acl.append((Allow, self.group_admin, 'g_admin'))

        members = self.id.users
        for member in members:
            acl.append((Allow, 'member:{}'.format(member.username), 'member'))

        # acl.append((Deny, Everyone, ALL_PERMISSIONS))

        return acl

    def __repr__(self):
        return "<Group(%s, location=%s)>" % (self.name, self.location)


class Discussion(Base, _Table):
    __tablename__ = 'discussion'
    title = Column(Text)
    group_id = Column(Integer, ForeignKey('groups.id'))
    posts = relationship('Post',
                         primaryjoin="(Discussion.id==Post.discussion_id)")

    def __repr__(self):
        return "<Discussion(%s)>" % (self.title)


class Post(Base, _Table):
    __tablename__ = 'post'
    text = Column(Text)
    discussion_id = Column(Integer, ForeignKey('discussion.id'))

    def __repr__(self):
        return "<Post(%s)>" % (self.text)


class Admin(Base, _Table):
    __tablename__ = 'admin'
    users = Column(Integer, ForeignKey('users.id'))
    group_id = Column(Integer, ForeignKey('groups.id'))

    def __repr__(self):
        return "<Admin(%s)>" % (self.users)
