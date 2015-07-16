# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime
from sqlalchemy import (
    Table,
    Column,
    Integer,
    Text,
    ForeignKey,
    Boolean,
    DateTime
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


groupdiscussion_table = Table('group_discussion', Base.metadata,
                              Column('group', Integer, ForeignKey('group.id')),
                              Column('discussion', Integer, ForeignKey(
                                     'discussion.id'))
                              )

grouppost_table = Table('group_post', Base.metadata,
                        Column('group', Integer, ForeignKey('group.id')),
                        Column('post', Integer, ForeignKey(
                               'post.id'))
                        )

discussiopost_table = Table('discussion_post',
                            Base.metadata,
                            Column('discussion', Integer,
                                   ForeignKey('discussion.id')),
                            Column('post', Integer, ForeignKey(
                                   'post.id'))
                            )

groupage_table = Table('group_age', Base.metadata, Column('group', Integer,
                       ForeignKey('group.id')), Column('agegroup', Integer,
                       ForeignKey('agegroup.id'))
                       )

groupuser_table = Table('group_user', Base.metadata, Column('group', Integer,
                        ForeignKey('group.id')), Column('users', Integer,
                        ForeignKey('users.id'))
                        )

groupcost_table = Table('group_cost', Base.metadata, Column('group_id',
                        Integer, ForeignKey('group.id')),
                        Column('cost_id', Integer, ForeignKey('cost.id'))
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


class User(Base, _Table):
    __tablename__ = 'users'
    username = Column(Text, nullable=False, unique=True)
    password = Column(Text, nullable=False)
    email = Column(Text, nullable=False, unique=True)
    firstname = Column(Text)
    lastname = Column(Text)
    confirmed = Column(Boolean, default=False)
    age = Column(Integer, ForeignKey('agegroup.id'))
    user_location = Column(Integer, ForeignKey('location.id'))
    cost = Column(Integer, ForeignKey('cost.id'))
    food_profile = relationship('Profile', secondary=usertaste_table,
                                backref='users')
    diet_restrict = relationship('Diet', secondary=userdiet_table,
                                 backref='users')
    user_grouups = relationship('Group', secondary=groupuser_table,
                                backref='users')
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
    def lookup_user_by_username(cls, username, session=None):
        if session is None:
            session = DBSession
        return session.query(cls).filter(User.username == username).one()

    @classmethod
    def lookup_user_by_id(cls, uid, session=None):
        if session is None:
            session = DBSession
        return session.query(cls).filter(cls.id == uid).one()

    @classmethod
    def change(cls, session=None, **kwargs):
        if session is None:
            session = DBSession
        instance = cls.lookup_user_by_username(username=kwargs["username"])
        instance.firstname = kwargs.get("firstname")
        instance.lastname = kwargs.get("lastname")
        instance.restaurants = kwargs.get("restaurant")
        instance.food = kwargs.get("food")
        tasteid = map(int, kwargs.get("taste"))
        dietid = map(int, kwargs.get("diet"))
        for eid in tasteid:
            instance.food_profile.append(session.query(Profile).filter
                                         (Profile.id == eid).all()[0])
        for eid in dietid:
            instance.food_profile.append(session.query(Diet).filter
                                         (Diet.id == eid).all()[0])
        instance.cost = int(kwargs.get("price"))
        instance.user_location = int(kwargs.get("location"))
        instance.age = int(kwargs.get("age"))
        session.add(instance)
        return instance

    def __repr__(self):
        return "<User({} {}, username={})>".format(self.firstname,
                                                   self.lastname,
                                                   self.username)


class Profile(Base, _Table):
    __tablename__ = 'profile'
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


class Group(Base, _Table):
    __tablename__ = 'group'
    name = Column(Text, nullable=False)
    description = Column(Text, nullable=False)
    location = Column(Integer, ForeignKey('location.id'))
    discussion = relationship('Discussion', secondary=groupdiscussion_table,
                              backref='group')
    group_admin = relationship("Admin", uselist=False, backref='group')

    def __repr__(self):
        return "<Group(%s, location=%s)>" % (self.name, self.location)


class Discussion(Base, _Table):
    __tablename__ = 'discussion'
    discussion_title = Column(Text)
    groupdiscussion = Column(Integer, ForeignKey('group.id'))

    @classmethod
    def group_lookup(cls, id=None, session=None):
        if session is None:
            session = DBSession
        return session.query(cls).filter(id == cls.groupdiscussion).all()

    def __repr__(self):
        return "<Discussion(%s)>" % (self.discussion_title)


class Post(Base, _Table):
    __tablename__ = 'post'
    discussionpost = Column(Integer, ForeignKey('discussion.id'))
    grouppost = Column(Integer, ForeignKey('group.id'))
    post_text = Column(Text)
    created = Column(DateTime, nullable=False,
                     default=datetime.datetime.utcnow)

    @classmethod
    def group_lookup(cls, id=None, session=None):
        if session is None:
            session = DBSession
        return session.query(cls).filter(id == cls.grouppost).all()

    def __repr__(self):
        return "<Post(%s)>" % (self.post_text)


class Admin(Base, _Table):
    __tablename__ = 'admin'
    users = Column(Integer, ForeignKey('users.id'))
    group_id = Column(Integer, ForeignKey('group.id'))

    def __repr__(self):
        return "<Admin(%s)>" % (self.users)
